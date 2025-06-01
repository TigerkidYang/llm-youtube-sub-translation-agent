from typing import TypedDict, Annotated, Sequence, List, Dict
from langchain_core.tools import tool # Ensure tool is imported if not already via langchain
from langgraph.graph.message import add_messages
from get_sub import list_available_languages, fetch_youtube_srt
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import os
import re # For SRT parsing

# Assuming prompts are defined in prompts.py
from prompts import (
    SUBTITLE_EXTRACTION_SYSTEM_PROMPT,
    TRANSLATION_CONTEXT_SYSTEM_PROMPT,
    TRANSLATION_CONTEXT_HUMAN_PROMPT,
    CHUNK_TRANSLATION_SYSTEM_PROMPT,
    CHUNK_TRANSLATION_HUMAN_PROMPT
)

load_dotenv()

# Constants
CHUNK_SIZE = 50

class AgentState(TypedDict):
    video_link: str
    original_language: str
    target_language: str
    
    # Fields for subtitle extraction flow
    available_languages: List | None
    chosen_language_code: str | None
    original_srt_path: str | None
    
    # Fields for translation flow
    sub_list: List[Dict[str, str]] | None # List of dicts: {'index': '', 'start_time': '', 'end_time': '', 'text': ''}
    sub_chunks_list: List[str] | None # List of combined text chunks
    current_chunk_index: int
    translation_memory: str | None
    translated_chunks_list: List[str] | None # List of translated text chunks
    translated_sub_list: List[Dict[str, str]] | None # Similar to sub_list, but with translated text
    final_srt_path: str | None # Path to the final translated SRT file
    
    messages: Annotated[Sequence[BaseMessage], add_messages]


def _parse_srt_to_list(srt_content: str) -> List[Dict[str, str]]:
    subs = []
    if not srt_content:
        return subs
    
    pattern = re.compile(
        r'(\d+)\s*\n'                         # Index
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*'  # Start time
        r'(\d{2}:\d{2}:\d{2},\d{3})\s*\n'     # End time
        r'((?:.+\n?)+)',                      # Text (one or more lines)
        re.MULTILINE
    )
    
    for match in pattern.finditer(srt_content):
        index = match.group(1)
        start_time = match.group(2)
        end_time = match.group(3)
        text = match.group(4).strip().replace('\r\n', '\n').replace('\r', '\n') 
        subs.append({
            'index': index,
            'start_time': start_time,
            'end_time': end_time,
            'text': text
        })
    return subs

def _list_to_srt_str(sub_list_data: List[Dict[str, str]]) -> str:
    srt_output = []
    for item in sub_list_data:
        srt_output.append(item['index'])
        srt_output.append(f"{item['start_time']} --> {item['end_time']}")
        srt_output.append(item['text'])
        srt_output.append("")
    return "\n".join(srt_output)


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
    return state

extraction_tools = [list_available_languages, fetch_youtube_srt]
llm = ChatOpenAI(model='gpt-4o').bind_tools(extraction_tools)
translation_llm = ChatOpenAI(model='gpt-4o')


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
    if not messages:
        return "end_process"
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "continue_extraction"
    return "end_process"

def prepare_translation_node(state: AgentState) -> dict:
    print("--- Preparing Translation ---")
    original_srt_path = state.get('original_srt_path')
    if not original_srt_path or not os.path.exists(original_srt_path):
        print(f"Error: Original SRT file not found at {original_srt_path}")
        return {"messages": [SystemMessage(content=f"Error: Original SRT file not found at {original_srt_path}. Cannot proceed with translation.")]}

    with open(original_srt_path, 'r', encoding='utf-8') as f:
        srt_content = f.read()
    
    sub_list = _parse_srt_to_list(srt_content)
    
    sub_chunks_list = []
    numbered_texts_for_chunking = [f"{item['index']}. {item['text']}" for item in sub_list]

    for i in range(0, len(numbered_texts_for_chunking), CHUNK_SIZE):
        chunk = numbered_texts_for_chunking[i:i + CHUNK_SIZE]
        sub_chunks_list.append("\n".join(chunk))

    return {
        "sub_list": sub_list,
        "sub_chunks_list": sub_chunks_list,
        "current_chunk_index": 0,
        "translated_chunks_list": []
    }

def generate_translation_context_node(state: AgentState) -> dict:
    print("--- Generating Translation Context ---")
    sub_list = state.get('sub_list')
    target_language = state.get('target_language')

    if not sub_list:
        return {"messages": [SystemMessage(content="Error: Subtitle list not found for context generation.")]}
    if not target_language:
        return {"messages": [SystemMessage(content="Error: Target language not found in state for context generation.")]}

    full_text = "\n".join([item['text'] for item in sub_list])
    
    system_prompt_formatted = TRANSLATION_CONTEXT_SYSTEM_PROMPT.format(target_language=target_language)
    human_prompt_formatted = TRANSLATION_CONTEXT_HUMAN_PROMPT.format(
        subtitle_full_text=full_text,
        target_language=target_language
    )
    
    context_messages = [
        SystemMessage(content=system_prompt_formatted),
        HumanMessage(content=human_prompt_formatted)
    ]
    
    ai_response = translation_llm.invoke(context_messages)
    translation_memory = ai_response.content
    
    return {"translation_memory": translation_memory}

def translate_current_chunk_node(state: AgentState) -> dict:
    print(f"--- Translating Chunk {state.get('current_chunk_index', 0) + 1} ---")
    current_chunk_index = state.get('current_chunk_index', 0)
    sub_chunks_list = state.get('sub_chunks_list')
    translation_memory = state.get('translation_memory')
    target_language = state.get('target_language')
    
    if not sub_chunks_list or current_chunk_index >= len(sub_chunks_list):
        return {"messages": [SystemMessage(content="Error: No more chunks to translate or invalid index.")]}
    if not target_language:
         return {"messages": [SystemMessage(content="Error: Target language not found in state for chunk translation.")]}
    if not translation_memory:
        return {"messages": [SystemMessage(content="Error: Translation memory not found in state for chunk translation.")]}

    current_chunk_text = sub_chunks_list[current_chunk_index]
    
    system_prompt_formatted = CHUNK_TRANSLATION_SYSTEM_PROMPT.format(target_language=target_language)
    human_prompt_formatted = CHUNK_TRANSLATION_HUMAN_PROMPT.format(
        translation_memory=translation_memory,
        target_language=target_language,
        numbered_subtitle_lines=current_chunk_text
    )

    chunk_translation_messages = [
        SystemMessage(content=system_prompt_formatted),
        HumanMessage(content=human_prompt_formatted)
    ]
    
    ai_response = translation_llm.invoke(chunk_translation_messages)
    translated_chunk_text = ai_response.content
    
    translated_chunks_list = state.get('translated_chunks_list', [])
    translated_chunks_list.append(translated_chunk_text)
    
    return {"translated_chunks_list": translated_chunks_list}

def aggregate_translation_node(state: AgentState) -> dict:
    print("--- Aggregating Translation (Incrementing Index) ---")
    current_chunk_index = state.get('current_chunk_index', 0)
    return {"current_chunk_index": current_chunk_index + 1}

def should_translate_more_chunks(state: AgentState) -> str:
    current_chunk_index = state.get('current_chunk_index', 0)
    sub_chunks_list = state.get('sub_chunks_list')
    
    if sub_chunks_list and current_chunk_index < len(sub_chunks_list):
        return "continue_translation"
    else:
        return "finish_translation"

def finalize_translation_node(state: AgentState) -> dict:
    print("--- Finalizing Translation ---")
    translated_chunks_list = state.get('translated_chunks_list')
    sub_list = state.get('sub_list') 
    original_srt_path = state.get('original_srt_path')
    
    if not translated_chunks_list or not sub_list or not original_srt_path:
        return {"messages": [SystemMessage(content="Error: Missing data for finalization.")]}

    full_translated_text_numbered = "\n".join(translated_chunks_list)
    
    # Attempt to strip common markdown code block delimiters
    cleaned_translated_text = full_translated_text_numbered.strip()
    if cleaned_translated_text.startswith("```") and cleaned_translated_text.endswith("```"):
        cleaned_translated_text = cleaned_translated_text[3:-3].strip()
        # Also remove potential language hint like ```plaintext
        if cleaned_translated_text.startswith("plaintext\n"):
            cleaned_translated_text = cleaned_translated_text[len("plaintext\n"):].strip()
        elif cleaned_translated_text.startswith("json\n"): # Or other languages
            cleaned_translated_text = cleaned_translated_text[len("json\n"):].strip()


    translated_lines_map: Dict[str, str] = {} 
    for line in cleaned_translated_text.splitlines():
        stripped_line = line.strip()
        if not stripped_line: # Skip empty lines after stripping
            continue
        
        match = re.match(r"(\d+)\.\s*(.*)", stripped_line)
        if match:
            original_index = match.group(1)
            translated_text = match.group(2).strip() # Strip text part too
            translated_lines_map[original_index] = translated_text
        else:
            # If a line doesn't match, but we are inside a block that should be translated lines,
            # it might be a continuation of a previous line if the LLM split a single subtitle entry
            # across multiple lines without repeating the number.
            # For now, we'll just warn. More sophisticated handling could be added.
            print(f"Warning: Could not parse translated line or format incorrect: '{line}'")

    translated_sub_list_output: List[Dict[str, str]] = []
    for original_item in sub_list:
        original_idx = original_item['index']
        translated_text_for_item = translated_lines_map.get(original_idx, original_item['text']) 
        
        translated_sub_list_output.append({
            'index': original_idx,
            'start_time': original_item['start_time'],
            'end_time': original_item['end_time'],
            'text': translated_text_for_item
        })
        
    final_srt_content = _list_to_srt_str(translated_sub_list_output)
    
    base, ext = os.path.splitext(original_srt_path)
    target_language_code = state.get('target_language', 'translated') 
    final_srt_file_path = f"{base}_{target_language_code}{ext}"
    
    with open(final_srt_file_path, 'w', encoding='utf-8') as f:
        f.write(final_srt_content)
    
    print(f"Translated SRT saved to: {final_srt_file_path}")
    return {
        "translated_sub_list": translated_sub_list_output,
        "final_srt_path": final_srt_file_path,
        "messages": [SystemMessage(content=f"Translation complete. Final SRT saved to {final_srt_file_path}")]
    }

graph = StateGraph(AgentState)

graph.add_node('input', input_node)
graph.add_node('getsub', get_sub_node)
extraction_tool_node = ToolNode(tools=extraction_tools)
graph.add_node('extraction_tools', extraction_tool_node)

graph.add_node('prepare_translation', prepare_translation_node)
graph.add_node('generate_translation_context', generate_translation_context_node)
graph.add_node('translate_current_chunk', translate_current_chunk_node)
graph.add_node('aggregate_translation', aggregate_translation_node)
graph.add_node('finalize_translation', finalize_translation_node)

graph.add_edge(START, 'input')
graph.add_edge('input', 'getsub')

graph.add_conditional_edges(
    'getsub',
    should_continue_extraction, 
    {
        'continue_extraction': 'extraction_tools',
        'start_translation': 'prepare_translation',
        'end_process': END
    }
)
graph.add_edge('extraction_tools', 'getsub')

graph.add_edge('prepare_translation', 'generate_translation_context')
graph.add_edge('generate_translation_context', 'translate_current_chunk')
graph.add_edge('translate_current_chunk', 'aggregate_translation')

graph.add_conditional_edges(
    'aggregate_translation',
    should_translate_more_chunks,
    {
        'continue_translation': 'translate_current_chunk',
        'finish_translation': 'finalize_translation'
    }
)
graph.add_edge('finalize_translation', END)

app = graph.compile()

if __name__ == '__main__':
    config = {"recursion_limit": 150} 
    initial_state = {} 

    for event in app.stream(initial_state, config=config):
        for k, v in event.items():
            if k != "__end__":
                print(f"Output from node: {k}")
                if 'messages' in v and v['messages']:
                    last_message = v['messages'][-1]
                    print(f"  Last Message Type: {last_message.type}, Content: {str(last_message.content)[:200]}...")
                if 'original_srt_path' in v and v['original_srt_path']:
                    print(f"  Original SRT Path: {v['original_srt_path']}")
                if 'final_srt_path' in v and v['final_srt_path']:
                    print(f"  Final Translated SRT Path: {v['final_srt_path']}")
                if 'current_chunk_index' in v and 'sub_chunks_list' in v and v['sub_chunks_list']:
                     if v['sub_chunks_list']: # Check if sub_chunks_list is not None and not empty
                        print(f"  Current Chunk Index: {v['current_chunk_index']} / {len(v['sub_chunks_list'])}")
                     else:
                        print(f"  Current Chunk Index: {v['current_chunk_index']} / (No chunks)")


                print("---")
        print("\n##################################################\n")

