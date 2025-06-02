from typing import TypedDict, Annotated, Sequence, List, Dict
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages
from get_sub import list_available_languages, fetch_youtube_srt # Assuming this is in the same directory
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import os
import re 

# Assuming prompts are defined in prompts.py and will be updated separately
from prompts import (
    SUBTITLE_EXTRACTION_SYSTEM_PROMPT,
    TRANSLATION_CONTEXT_SYSTEM_PROMPT,
    TRANSLATION_CONTEXT_HUMAN_PROMPT,
    CHUNK_TRANSLATION_SYSTEM_PROMPT, # This prompt will need adjustment
    CHUNK_TRANSLATION_HUMAN_PROMPT
)

load_dotenv()

# Constants
CHUNK_SIZE = 50 # Keeping this as is from the "markdown check" version for now
MAX_TRANSLATION_RETRIES = 2 

class AgentState(TypedDict):
    video_link: str
    original_language: str
    target_language: str
    
    available_languages: List | None
    chosen_language_code: str | None
    original_srt_path: str | None
    
    sub_list: List[Dict[str, str]] | None 
    sub_chunks_list: List[str] | None 
    current_chunk_index: int 
    translation_memory: str | None
    translated_chunks_list: List[str] | None 
    translated_sub_list: List[Dict[str, str]] | None 
    final_srt_path: str | None 
    
    current_chunk_original_text: str | None 
    current_chunk_translated_text: str | None 
    current_chunk_validation_status: str | None 
    current_chunk_retry_count: int 
    
    messages: Annotated[Sequence[BaseMessage], add_messages]


def _parse_srt_to_list(srt_content: str) -> List[Dict[str, str]]:
    subs = []
    if not srt_content:
        return subs
    pattern = re.compile(
        r'(\d+)\s*\n'
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*'
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*\n'
        r'((?:.+\n?)+)', 
        re.MULTILINE
    )
    for match in pattern.finditer(srt_content):
        index = match.group(1)
        start_time = match.group(2)
        end_time = match.group(3)
        # MODIFICATION: Join multi-line text into a single line with spaces
        text_lines = match.group(4).strip().splitlines()
        single_line_text = " ".join(line.strip() for line in text_lines if line.strip())
        
        subs.append({
            'index': index,
            'start_time': start_time,
            'end_time': end_time,
            'text': single_line_text # Store as single line
        })
    return subs

def _list_to_srt_str(sub_list_data: List[Dict[str, str]]) -> str:
    srt_output = []
    for item in sub_list_data:
        srt_output.append(item['index'])
        srt_output.append(f"{item['start_time']} --> {item['end_time']}")
        # Text is expected to be single line here due to preprocessing,
        # but if LLM re-introduces newlines for translated long lines,
        # SRT standard allows multi-line text per entry.
        srt_output.append(item['text']) 
        srt_output.append("")
    return "\n".join(srt_output)

def _clean_llm_output(text: str) -> str:
    cleaned = text.strip()
    code_block_match = re.match(r"^```(?:[a-zA-Z0-9_.-]*)?\s*\n(.*?)\n```$", cleaned, re.DOTALL | re.MULTILINE)
    if code_block_match:
        cleaned = code_block_match.group(1).strip()
    else: 
        if cleaned.startswith("```") and cleaned.endswith("```"):
            cleaned = cleaned[3:-3].strip() 
    return cleaned


def input_node(state: AgentState) -> AgentState:
    video_link = input('Enter the youtube link: ')
    state['video_link'] = video_link
    original_language = input('What language of sub you want to translate? ')
    state['original_language'] = original_language
    target_language = input('What language sub do you want? ')
    state['target_language'] = target_language

    system_prompt_text = SUBTITLE_EXTRACTION_SYSTEM_PROMPT
    human_message_content = (
        f"Video URL: {state['video_link']}, "
        f"Original Language: {state['original_language']}, "
        f"Target Language: {state['target_language']}"
    )
    initial_messages = [
        SystemMessage(content=system_prompt_text),
        HumanMessage(content=human_message_content)
    ]
    state['messages'] = initial_messages
    state['sub_list'] = None
    state['sub_chunks_list'] = None
    state['current_chunk_index'] = 0
    state['translation_memory'] = None
    state['translated_chunks_list'] = [] 
    state['translated_sub_list'] = None
    state['final_srt_path'] = None
    state['current_chunk_original_text'] = None
    state['current_chunk_translated_text'] = None
    state['current_chunk_validation_status'] = None
    state['current_chunk_retry_count'] = 0
    return state

extraction_tools = [list_available_languages, fetch_youtube_srt]
llm = ChatOpenAI(model='o3-mini').bind_tools(extraction_tools)
translation_llm = ChatOpenAI(model='o3-mini') 

def get_sub_node(state: AgentState) -> dict:
    messages = state['messages']
    updates_to_state = {}
    if messages and isinstance(messages[-1], ToolMessage):
        last_message = messages[-1]
        if last_message.name == "list_available_languages":
            updates_to_state["available_languages"] = last_message.content
        elif last_message.name == "fetch_youtube_srt":
            updates_to_state["original_srt_path"] = last_message.content
    ai_response = llm.invoke(messages)
    updates_to_state["messages"] = [ai_response]
    if ai_response.tool_calls:
        for tool_call in ai_response.tool_calls:
            if tool_call['name'] == "fetch_youtube_srt":
                if isinstance(tool_call['args'], dict):
                    updates_to_state["chosen_language_code"] = tool_call['args'].get('language_code')
                break
    return updates_to_state

def should_continue_extraction(state: AgentState) -> str:
    if state.get("original_srt_path") is not None:
        return "start_translation" 
    messages = state['messages']
    if not messages: return "end_process"
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "continue_extraction"
    return "end_process"

def prepare_translation_node(state: AgentState) -> dict:
    print("--- Preparing Translation ---")
    original_srt_path = state.get('original_srt_path')
    if not original_srt_path or not os.path.exists(original_srt_path):
        print(f"Error: Original SRT file not found at {original_srt_path}")
        return {"messages": [SystemMessage(content=f"Error: Original SRT file not found. Cannot proceed.")]}
    with open(original_srt_path, 'r', encoding='utf-8') as f: srt_content = f.read()
    
    # _parse_srt_to_list now converts multi-line text to single-line
    sub_list = _parse_srt_to_list(srt_content) 
    
    # Each item['text'] in sub_list is now single-line.
    # So, each f-string in numbered_texts_for_chunking will also represent a single line of original text.
    numbered_texts_for_chunking = [f"{item['index']}. {item['text']}" for item in sub_list]
    
    sub_chunks_list = ["\n".join(numbered_texts_for_chunking[i:i + CHUNK_SIZE]) 
                       for i in range(0, len(numbered_texts_for_chunking), CHUNK_SIZE)]
    return {
        "sub_list": sub_list, "sub_chunks_list": sub_chunks_list, 
        "current_chunk_index": 0, "translated_chunks_list": [], 
        "current_chunk_retry_count": 0 
    }

def generate_translation_context_node(state: AgentState) -> dict:
    print("--- Generating Translation Context ---")
    sub_list, target_language = state.get('sub_list'), state.get('target_language')
    if not sub_list: return {"messages": [SystemMessage(content="Error: Subtitle list not found.")]}
    if not target_language: return {"messages": [SystemMessage(content="Error: Target language not found.")]}
    
    # Texts in sub_list are now single-lined per entry
    full_text = "\n".join([item['text'] for item in sub_list]) 
    
    sys_prompt = TRANSLATION_CONTEXT_SYSTEM_PROMPT.format(target_language=target_language)
    human_prompt = TRANSLATION_CONTEXT_HUMAN_PROMPT.format(subtitle_full_text=full_text, target_language=target_language)
    ai_response = translation_llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=human_prompt)])
    return {"translation_memory": ai_response.content}

def translate_current_chunk_node(state: AgentState) -> dict:
    idx = state.get('current_chunk_index', 0)
    retry_count = state.get('current_chunk_retry_count', 0)
    print(f"--- Translating Chunk {idx + 1} (Attempt {retry_count + 1}) ---")
    sub_chunks_list = state.get('sub_chunks_list')
    
    if not sub_chunks_list or idx >= len(sub_chunks_list):
        return {"messages": [SystemMessage(content="Error: No more chunks or invalid index.")]}

    current_original_chunk_text = sub_chunks_list[idx] # This chunk now contains single-line entries
    translation_memory, target_language = state.get('translation_memory'), state.get('target_language')

    if not target_language: return {"messages": [SystemMessage(content="Error: Target language missing.")]}
    if not translation_memory: return {"messages": [SystemMessage(content="Error: Translation memory missing.")]}

    retry_note = ""
    if retry_count > 0:
        retry_note = "\n\nIMPORTANT: YOUR PREVIOUS ATTEMPT WAS REJECTED BECAUSE IT CONTAINED MARKDOWN CODE BLOCK DELIMITERS (```). PLEASE PROVIDE THE TRANSLATION AS PLAIN TEXT, STRICTLY FOLLOWING THE NUMBERED LINE FORMAT WITHOUT ANY CODE BLOCK WRAPPERS."

    # The CHUNK_TRANSLATION_SYSTEM_PROMPT might need slight adjustment
    # to reflect that input lines are now guaranteed to be single lines of text.
    sys_prompt = CHUNK_TRANSLATION_SYSTEM_PROMPT.format(target_language=target_language) + retry_note
    human_prompt = CHUNK_TRANSLATION_HUMAN_PROMPT.format(
        translation_memory=translation_memory, 
        target_language=target_language, 
        numbered_subtitle_lines=current_original_chunk_text
    )
    ai_response = translation_llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=human_prompt)])
    
    return {
        "current_chunk_original_text": current_original_chunk_text, 
        "current_chunk_translated_text": ai_response.content,
        "current_chunk_validation_status": "PENDING_VALIDATION"
    }

def validate_translation_format_node(state: AgentState) -> dict:
    chunk_idx = state.get('current_chunk_index', 0)
    print(f"--- Validating Chunk {chunk_idx + 1} for Markdown Blocks ---")
    raw_translated_chunk_text = state.get('current_chunk_translated_text') 
    retry_count = state.get('current_chunk_retry_count', 0)

    if raw_translated_chunk_text is None:
        print(f"Error for Chunk {chunk_idx + 1}: Missing translated text for validation.")
        return {"current_chunk_validation_status": "INVALID_MAX_RETRIES_REACHED"} 

    if "```" in raw_translated_chunk_text:
        print(f"Validation Error for Chunk {chunk_idx + 1}: Markdown code block '```' detected.")
        is_valid_format = False
    else:
        is_valid_format = True 

    if is_valid_format:
        print(f"Validation for Chunk {chunk_idx + 1}: PASSED (No Markdown Blocks).")
        cleaned_text = _clean_llm_output(raw_translated_chunk_text) # Clean even if passed, for safety
        return {
            "current_chunk_validation_status": "VALID", 
            "current_chunk_translated_text": cleaned_text 
        }
    else:
        print(f"Validation for Chunk {chunk_idx + 1}: FAILED (Markdown Block Detected) (Retry {retry_count + 1})")
        if retry_count >= MAX_TRANSLATION_RETRIES:
            print(f"Max retries ({MAX_TRANSLATION_RETRIES}) reached for chunk {chunk_idx + 1} due to markdown blocks.")
            return {"current_chunk_validation_status": "INVALID_MAX_RETRIES_REACHED"}
        else:
            return {
                "current_chunk_validation_status": "INVALID_NEEDS_RETRY",
                "current_chunk_retry_count": retry_count + 1
            }

def decide_after_validation(state: AgentState) -> str:
    status = state.get('current_chunk_validation_status')
    chunk_idx = state.get('current_chunk_index', 0)
    if status == "VALID":
        return "proceed_to_aggregate"
    elif status == "INVALID_NEEDS_RETRY":
        return "retry_chunk_translation"
    elif status == "INVALID_MAX_RETRIES_REACHED":
        print(f"Warning: Chunk {chunk_idx + 1} translation failed after max retries (markdown block issue). Using original text as placeholder.")
        return "proceed_to_aggregate_with_placeholder" 
    else: 
        print(f"Error: Unknown validation status '{status}' for chunk {chunk_idx + 1}. Ending process.")
        return END 

def aggregate_translation_node(state: AgentState) -> dict:
    chunk_idx = state.get('current_chunk_index', 0)
    print(f"--- Aggregating Chunk {chunk_idx + 1} ---")
    translated_chunks_list = state.get('translated_chunks_list', [])
    text_to_append_for_aggregation = state.get('current_chunk_translated_text') 
    validation_status = state.get('current_chunk_validation_status')

    if validation_status == "INVALID_MAX_RETRIES_REACHED":
        original_text = state.get('current_chunk_original_text', "[ERROR: Placeholder - Original Text Missing]")
        text_to_append_for_aggregation = f"[TRANSLATION FAILED (MARKDOWN BLOCK) - ORIGINAL TEXT BELOW]\n{original_text}"
        print(f"Appended original text for chunk {chunk_idx + 1} due to max retries (markdown block).")
    elif validation_status == "VALID":
        if text_to_append_for_aggregation is None: 
             original_text = state.get('current_chunk_original_text', "[ERROR: Placeholder - Original Text Missing]")
             text_to_append_for_aggregation = f"[ERROR: VALID BUT TEXT MISSING - ORIGINAL TEXT BELOW]\n{original_text}"
             print(f"Warning: Chunk {chunk_idx + 1} was VALID but translated text is None. Appending placeholder.")
    else: 
        original_text = state.get('current_chunk_original_text', "[ERROR: Placeholder - Original Text Missing]")
        text_to_append_for_aggregation = f"[ERROR: UNEXPECTED VALIDATION STATUS ({validation_status}) - ORIGINAL TEXT BELOW]\n{original_text}"
        print(f"Warning: Chunk {chunk_idx + 1} had unexpected status '{validation_status}'. Appending placeholder.")
    
    translated_chunks_list.append(text_to_append_for_aggregation)
    new_index = chunk_idx + 1
    return {
        "translated_chunks_list": translated_chunks_list,
        "current_chunk_index": new_index,
        "current_chunk_retry_count": 0 
    }

def should_translate_more_chunks(state: AgentState) -> str: 
    current_chunk_index = state.get('current_chunk_index', 0)
    sub_chunks_list = state.get('sub_chunks_list')
    if sub_chunks_list and current_chunk_index < len(sub_chunks_list):
        return "translate_next_chunk" 
    else:
        return "finish_translation" 

def finalize_translation_node(state: AgentState) -> dict:
    print("--- Finalizing Translation ---")
    translated_chunks_list = state.get('translated_chunks_list')
    sub_list = state.get('sub_list') 
    original_srt_path = state.get('original_srt_path')
    
    if not sub_list: 
        print("Warning: No original subtitles to finalize.")
        return {"messages": [SystemMessage(content="No subtitles to finalize.")]}
    if not translated_chunks_list : 
         print("Warning: No translated chunks to finalize. Using original subtitles.")
    
    full_text_to_parse = "\n".join(translated_chunks_list)
    
    translated_lines_map: Dict[str, str] = {} 
    # Since input to LLM is now guaranteed single-line per numbered entry,
    # and we expect LLM to output single-line per numbered entry,
    # this simple parsing in finalize might work better.
    # Warnings will still occur if LLM fails to provide "number. text" for any line.
    for line in full_text_to_parse.splitlines():
        stripped_line = line.strip()
        if not stripped_line: continue
        
        match = re.match(r"(\d+)\.\s*(.*)", stripped_line) 
        if match:
            original_index = match.group(1)
            translated_text = match.group(2) 
            translated_lines_map[original_index] = translated_text
        elif not (stripped_line.startswith("[TRANSLATION FAILED") or stripped_line.startswith("[ERROR:")):
            print(f"Warning: Finalize - Could not parse line: '{line}'")

    translated_sub_list_output: List[Dict[str, str]] = []
    for original_item in sub_list: # original_item['text'] is now single-line
        original_idx = original_item['index']
        translated_text_for_item = translated_lines_map.get(original_idx, original_item['text']) 
        
        translated_sub_list_output.append({
            'index': original_idx, 'start_time': original_item['start_time'],
            'end_time': original_item['end_time'], 'text': translated_text_for_item
        })
        
    final_srt_content = _list_to_srt_str(translated_sub_list_output)
    base, ext = os.path.splitext(original_srt_path)
    target_lang_code = state.get('target_language', 'translated') 
    final_srt_path = f"{base}_{target_lang_code}{ext}"
    with open(final_srt_path, 'w', encoding='utf-8') as f: f.write(final_srt_content)
    print(f"Translated SRT saved to: {final_srt_path}")
    return {
        "translated_sub_list": translated_sub_list_output, "final_srt_path": final_srt_path,
        "messages": [SystemMessage(content=f"Translation complete. Final SRT saved to {final_srt_path}")]
    }

# Graph definition (remains the same as the previous version with markdown check)
graph = StateGraph(AgentState)
graph.add_node('input', input_node)
graph.add_node('getsub', get_sub_node)
extraction_tool_node = ToolNode(tools=extraction_tools)
graph.add_node('extraction_tools', extraction_tool_node)
graph.add_node('prepare_translation', prepare_translation_node)
graph.add_node('generate_translation_context', generate_translation_context_node)
graph.add_node('translate_current_chunk', translate_current_chunk_node)
graph.add_node('validate_translation_format', validate_translation_format_node) 
graph.add_node('aggregate_translation', aggregate_translation_node)
graph.add_node('finalize_translation', finalize_translation_node)
graph.add_edge(START, 'input')
graph.add_edge('input', 'getsub')
graph.add_conditional_edges(
    'getsub', should_continue_extraction, 
    {"continue_extraction": 'extraction_tools', "start_translation": 'prepare_translation', "end_process": END}
)
graph.add_edge('extraction_tools', 'getsub')
graph.add_edge('prepare_translation', 'generate_translation_context')
graph.add_conditional_edges(
    'generate_translation_context', 
    should_translate_more_chunks, 
    {
        "translate_next_chunk": 'translate_current_chunk',
        "finish_translation": 'finalize_translation' 
    }
)
graph.add_edge('translate_current_chunk', 'validate_translation_format')
graph.add_conditional_edges(
    'validate_translation_format',
    decide_after_validation,
    {
        "retry_chunk_translation": 'translate_current_chunk', 
        "proceed_to_aggregate": 'aggregate_translation',
        "proceed_to_aggregate_with_placeholder": 'aggregate_translation'
    }
)
graph.add_conditional_edges(
    'aggregate_translation',
    should_translate_more_chunks, 
    {
        "translate_next_chunk": 'translate_current_chunk', 
        "finish_translation": 'finalize_translation'      
    }
)
graph.add_edge('finalize_translation', END)

app = graph.compile()

if __name__ == '__main__':
    config = {"recursion_limit": 250} 
    initial_state = {} 
    for event in app.stream(initial_state, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(f"Output from node: {k}")
                if 'messages' in v and v['messages']:
                    last_message = v['messages'][-1]
                    print(f"  Last Msg: {last_message.type}, Content: {str(last_message.content)[:100]}...")
                if 'original_srt_path' in v and v['original_srt_path']:
                    print(f"  Original SRT: {v['original_srt_path']}")
                if 'final_srt_path' in v and v['final_srt_path']:
                    print(f"  Final SRT: {v['final_srt_path']}")
                if 'sub_chunks_list' in v and v['sub_chunks_list'] is not None:
                    chunk_len = len(v['sub_chunks_list']) if v['sub_chunks_list'] else 0
                    idx = v.get('current_chunk_index',0)
                    retry = v.get('current_chunk_retry_count',0)
                    status = v.get('current_chunk_validation_status','')
                    print(f"  Chunk Prog: {idx}/{chunk_len}, Retry: {retry}, Status: {status}")
                print("---")
        print("\n##################################################\n")
