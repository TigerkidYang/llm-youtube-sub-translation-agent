from typing import TypedDict, Annotated, Sequence, List, Dict
from langchain_core.tools import tool 
from langgraph.graph.message import add_messages
from get_sub import list_available_languages, fetch_youtube_srt
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
import os
import re 

from prompts import (
    SUBTITLE_EXTRACTION_SYSTEM_PROMPT,
    TRANSLATION_CONTEXT_SYSTEM_PROMPT,
    TRANSLATION_CONTEXT_HUMAN_PROMPT,
    CHUNK_TRANSLATION_SYSTEM_PROMPT,
    CHUNK_TRANSLATION_HUMAN_PROMPT
)

load_dotenv()

# Constants
CHUNK_SIZE = 50 # Number of subtitle entries per translation chunk.
MAX_TRANSLATION_RETRIES = 2 # Maximum retry attempts for translating a chunk. 

class AgentState(TypedDict):
    video_link: str # URL of the YouTube video to be translated.
    original_language: str # User's stated original language preference (e.g., 'English', 'en')
    target_language: str # Desired language for the translated subtitles.
    
    available_languages: List[Dict[str, any]] | None # Stores list of {'name': str, 'code': str, 'is_generated': bool}
    chosen_language_code: str | None # The language code selected by the user from available_languages
    original_srt_path: str | None # File path to the downloaded original SRT subtitles.
    
    sub_list: List[Dict[str, str]] | None # List of dictionaries representing original subtitle entries. 
    sub_chunks_list: List[str] | None # Original subtitles divided into processable text chunks. 
    current_chunk_index: int # Index of the current subtitle chunk being processed. 
    translation_memory: str | None # Contextual information or glossary for consistent translation.
    translated_chunks_list: List[str] | None # List of translated subtitle text chunks. 
    translated_sub_list: List[Dict[str, str]] | None # List of dictionaries representing translated subtitle entries. 
    final_srt_path: str | None # File path to the final translated SRT subtitles. 
    
    current_chunk_original_text: str | None # Text of the original subtitle chunk currently being translated. 
    current_chunk_translated_text: str | None # Text of the translated subtitle chunk. 
    current_chunk_validation_status: str | None # Status of the current chunk's translation validation (e.g., 'valid', 'invalid'). 
    current_chunk_retry_count: int # Number of retry attempts for the current translation chunk. 
    
    messages: Annotated[Sequence[BaseMessage], add_messages] # History of messages in the LangGraph agent execution.


def _parse_srt_to_list(srt_content: str) -> List[Dict[str, str]]:
    """Parses SRT formatted string content into a list of subtitle dictionaries."""
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
    """Converts a list of subtitle dictionaries back into an SRT formatted string."""
    srt_output = []
    for item in sub_list_data:
        srt_output.append(item['index'])
        srt_output.append(f"{item['start_time']} --> {item['end_time']}")
        # Ensures SRT compliance, allowing multi-line text if reintroduced by LLM.
        srt_output.append(item['text']) 
        srt_output.append("")
    return "\n".join(srt_output)

def _clean_llm_output(text: str) -> str:
    """Cleans LLM output by removing markdown code blocks and surrounding quotes."""
    cleaned = text.strip()
    code_block_match = re.match(r"^```(?:[a-zA-Z0-9_.-]*)?\s*\n(.*?)\n```$", cleaned, re.DOTALL | re.MULTILINE)
    if code_block_match:
        cleaned = code_block_match.group(1).strip()
    else: 
        if cleaned.startswith("```") and cleaned.endswith("```"):
            cleaned = cleaned[3:-3].strip() 
    return cleaned


def get_video_link_node(state: AgentState) -> AgentState:
    """Prompts the user to input a YouTube video link and updates the state."""
    logger.info("Entering node: get_video_link_node")
    video_link = input('Please enter the YouTube video link: ')
    logger.info(f"User provided video link: {video_link}")
    return {"video_link": video_link, "messages": [HumanMessage(content=f"Video link provided: {video_link}")]}

def display_available_languages_node(state: AgentState) -> AgentState:
    """Fetches and displays available subtitle languages for the video, then updates the state."""
    logger.info("Entering node: display_available_languages_node")
    video_url = state['video_link']
    if not video_url:
        logger.error("Video link is missing.")
        return {"available_languages": None, "messages": state.get('messages', []) + [SystemMessage(content="Error: Video link is missing.")]}
    
    try:
        logger.info(f"Fetching available languages for: {video_url}")
        # Directly call the tool function using .invoke()
        available_langs_list = list_available_languages.invoke({"video_url": video_url})
        
        if not available_langs_list:
            logger.warning(f"No subtitles found for video: {video_url}")
            print("Sorry, no subtitles seem to be available for this video.")
            return {"available_languages": None, "messages": state.get('messages', []) + [SystemMessage(content="No available subtitles found.")]}
        
        print("\nAvailable subtitle languages for the video:")
        for lang_info in available_langs_list:
            print(f"  - {lang_info['name']} (Code: {lang_info['code']}){' (Autogenerated)' if lang_info.get('is_generated') else ''}")
        print("")
        logger.info(f"Successfully fetched and displayed available languages: {available_langs_list}")
        return {"available_languages": available_langs_list, "messages": state.get('messages', []) + [SystemMessage(content=f"Available languages displayed: {available_langs_list}")]}
    except Exception as e:
        logger.error(f"Error fetching or displaying available languages: {e}", exc_info=True)
        print(f"Error fetching available languages: {e}")
        return {"available_languages": None, "messages": state.get('messages', []) + [SystemMessage(content=f"Error fetching available languages: {e}")]}

def decide_after_displaying_languages(state: AgentState) -> str:
    """Determines the next step based on whether available languages were found."""
    logger.info("Entering node: decide_after_displaying_languages")
    if state.get('available_languages'):
        logger.info("Available languages found, proceeding to get language choices.")
        return "get_language_choices"
    else:
        logger.warning("No available languages, or error occurred. Ending process.")
        return END

def get_language_choices_node(state: AgentState) -> AgentState:
    """Prompts user for original and target language choices, then prepares state for subtitle extraction."""
    logger.info("Entering node: get_language_choices_node")
    available_languages_list = state['available_languages']
    if not available_languages_list: # Should not happen if decide_after_displaying_languages works
        logger.error("Cannot get language choices, no available_languages_list in state.")
        return { "messages": state.get('messages', []) + [SystemMessage(content="Internal error: available languages list not found.")]}

    available_codes = [lang['code'] for lang in available_languages_list]
    chosen_code = ""
    original_language_name = ""

    while True:
        original_language_code_input = input('Enter the language code of the original subtitles you want to translate: ').strip()
        if original_language_code_input in available_codes:
            chosen_code = original_language_code_input
            # Find the full name for the chosen code
            for lang_info in available_languages_list:
                if lang_info['code'] == chosen_code:
                    original_language_name = lang_info['name']
                    break
            break
        else:
            print(f"Invalid language code '{original_language_code_input}'. Please choose from the available codes listed above.")
    
    # Get the target language from the user
    target_language = input('Enter the target language you want to translate to (e.g., en, zh-CN, fr): ').strip()
    
    # Update the state with the user's language choices
    state['chosen_language_code'] = chosen_code
    # Use the full name if found, otherwise default to the code itself
    state['original_language'] = original_language_name if original_language_name else chosen_code 
    state['target_language'] = target_language

    logger.info(f"User chose original language code: {chosen_code}, target language: {target_language}")
    
    # Prepare messages for the subtitle extraction agent (get_sub_node)
    extraction_messages = [
        SystemMessage(content=SUBTITLE_EXTRACTION_SYSTEM_PROMPT),
        HumanMessage(content=f"Please fetch subtitles for the video: {state['video_link']}. "
                             f"The chosen original language code is '{chosen_code}'.")
    ]
    
    # Reset relevant parts of state for the new process
    return {
        "video_link": state['video_link'],
        "original_language": state['original_language'],
        "target_language": target_language,
        "available_languages": available_languages_list,
        "chosen_language_code": chosen_code,
        "messages": extraction_messages,
        "current_chunk_index": 0,
        "current_chunk_retry_count": 0,
        "translated_chunks_list": [],
        "translated_sub_list": [],
        "original_srt_path": None,
        "sub_list": None,
        "sub_chunks_list": None,
        "translation_memory": None,
        "current_chunk_original_text": None,
        "current_chunk_translated_text": None,
        "current_chunk_validation_status": None,
        "final_srt_path": None
    }

# Tools for the subtitle extraction agent (get_sub_node). Only fetch_youtube_srt is needed now.
extraction_tools = [fetch_youtube_srt]
llm = ChatOpenAI(model='o3-mini').bind_tools(extraction_tools)
translation_llm = ChatOpenAI(model='o3-mini') 

def get_sub_node(state: AgentState) -> AgentState:
    """Invokes the LLM to extract subtitles using the chosen language and video link."""
    logger.info("Entering node: get_sub_node")
    logger.info(f"Invoking LLM for subtitle extraction with messages: {state['messages']}")
    response = llm.invoke(state['messages'])
    logger.info(f"LLM response for subtitle extraction: {response}")
    new_messages = state.get('messages', []) + [response]
    current_original_srt_path = state.get('original_srt_path') # Get existing path if any

    # If the LLM's response is a final text message (not a tool call)
    if isinstance(response, AIMessage) and not response.tool_calls:
        logger.info(f"get_sub_node: LLM provided final text response: {response.content}")
        # Attempt to extract SRT path from LLM's final text response if no tool call.
        pattern = r"""['"]?(transcripts/([a-zA-Z0-9_]|-)+\.srt)['"]?"""
        match = re.search(pattern, response.content)
        if match:
            extracted_path = match.group(1)
            logger.info(f"get_sub_node: Extracted SRT path from final AIMessage content: {extracted_path}")
            current_original_srt_path = extracted_path
        else:
            logger.warning(f"get_sub_node: Could not extract SRT path from final AIMessage content: {response.content}")
    
    logger.info(f"get_sub_node: Value of original_srt_path before returning state: '{current_original_srt_path}'")
    return {
        "messages": new_messages,
        "original_srt_path": current_original_srt_path
    }

def should_continue_extraction(state: AgentState) -> str:
    """Determines if subtitle extraction requires a tool call, or can proceed to translation/end."""
    if state.get("original_srt_path") is not None:
        return "start_translation" 
    messages = state['messages']
    if not messages: return "end_process"
    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "continue_extraction"
    return "end_process"

def prepare_translation_node(state: AgentState) -> dict:
    """Loads original subtitles, parses them, and divides them into text chunks for translation."""
    logger.info("Preparing translation...")
    original_srt_path = state.get('original_srt_path')
    if not original_srt_path or not os.path.exists(original_srt_path):
        logger.error(f"Error reading SRT file {original_srt_path}: File not found")
        return {"messages": [SystemMessage(content=f"Error: Original SRT file not found. Cannot proceed.")]}
    with open(original_srt_path, 'r', encoding='utf-8') as f: srt_content = f.read()
    
    sub_list = _parse_srt_to_list(srt_content) 
    
    numbered_texts_for_chunking = [f"{item['index']}. {item['text']}" for item in sub_list]
    
    sub_chunks_list = ["\n".join(numbered_texts_for_chunking[i:i + CHUNK_SIZE]) 
                       for i in range(0, len(numbered_texts_for_chunking), CHUNK_SIZE)]
    logger.info(f"Created {len(sub_chunks_list)} chunks of size {CHUNK_SIZE}.")
    return {
        "sub_list": sub_list, "sub_chunks_list": sub_chunks_list, 
        "current_chunk_index": 0, "translated_chunks_list": [], 
        "current_chunk_retry_count": 0 
    }

def generate_translation_context_node(state: AgentState) -> dict:
    """Generates a contextual translation memory from the full subtitle text using an LLM."""
    logger.info("Generating translation context...")
    sub_list, target_language = state.get('sub_list'), state.get('target_language')
    if not sub_list: return {"messages": [SystemMessage(content="Error: Subtitle list not found.")]}
    if not target_language: return {"messages": [SystemMessage(content="Error: Target language not found.")]}
    
    full_text = "\n".join([item['text'] for item in sub_list]) 
    
    sys_prompt = TRANSLATION_CONTEXT_SYSTEM_PROMPT.format(target_language=target_language)
    human_prompt = TRANSLATION_CONTEXT_HUMAN_PROMPT.format(subtitle_full_text=full_text, target_language=target_language)
    ai_response = translation_llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=human_prompt)])
    logger.info(f"LLM generated translation memory (first 200 chars): {ai_response.content[:200]}...")
    return {"translation_memory": ai_response.content}

def translate_current_chunk_node(state: AgentState) -> dict:
    """Translates the current chunk of subtitles using an LLM, incorporating translation memory and retry logic."""
    idx = state.get('current_chunk_index', 0)
    retry_count = state.get('current_chunk_retry_count', 0)
    logger.info(f"Translating chunk {idx + 1} (Attempt {retry_count + 1})...")
    sub_chunks_list = state.get('sub_chunks_list')
    
    if not sub_chunks_list or idx >= len(sub_chunks_list):
        return {"messages": [SystemMessage(content="Error: No more chunks or invalid index.")]}
    current_original_chunk_text = sub_chunks_list[idx]
    translation_memory, target_language = state.get('translation_memory'), state.get('target_language')

    if not target_language: return {"messages": [SystemMessage(content="Error: Target language missing.")]}
    if not translation_memory: return {"messages": [SystemMessage(content="Error: Translation memory missing.")]}
    retry_note = ""
    if retry_count > 0:
        retry_note = "\n\nIMPORTANT: YOUR PREVIOUS ATTEMPT WAS REJECTED BECAUSE IT CONTAINED MARKDOWN CODE BLOCK DELIMITERS (```). PLEASE PROVIDE THE TRANSLATION AS PLAIN TEXT, STRICTLY FOLLOWING THE NUMBERED LINE FORMAT WITHOUT ANY CODE BLOCK WRAPPERS."
    sys_prompt = CHUNK_TRANSLATION_SYSTEM_PROMPT.format(target_language=target_language) + retry_note
    human_prompt = CHUNK_TRANSLATION_HUMAN_PROMPT.format(
        translation_memory=translation_memory, 
        target_language=target_language, 
        numbered_subtitle_lines=current_original_chunk_text
    )
    ai_response = translation_llm.invoke([SystemMessage(content=sys_prompt), HumanMessage(content=human_prompt)])
    logger.debug(f"Raw LLM output for chunk (first 200 chars): {ai_response.content[:200]}...")
    return {
        "current_chunk_original_text": current_original_chunk_text, 
        "current_chunk_translated_text": ai_response.content,
        "current_chunk_validation_status": "PENDING_VALIDATION"
    }

def validate_translation_format_node(state: AgentState) -> dict:
    """Validates the format of the translated chunk, checking for markdown code blocks."""
    chunk_idx = state.get('current_chunk_index', 0)
    logger.info(f"Validating translation format for chunk {chunk_idx + 1}...")
    raw_translated_chunk_text = state.get('current_chunk_translated_text') 
    retry_count = state.get('current_chunk_retry_count', 0)

    if raw_translated_chunk_text is None:
        logger.error(f"Error for Chunk {chunk_idx + 1}: Missing translated text for validation.")
        return {"current_chunk_validation_status": "INVALID_MAX_RETRIES_REACHED"} 

    if "```" in raw_translated_chunk_text:
        logger.warning(f"Validation Error for Chunk {chunk_idx + 1}: Markdown code block '```' detected.")
        is_valid_format = False
    else:
        is_valid_format = True 

    if is_valid_format:
        logger.info(f"Validation for Chunk {chunk_idx + 1}: PASSED (No Markdown Blocks).")
        cleaned_text = _clean_llm_output(raw_translated_chunk_text) # Clean even if passed, for safety
        return {
            "current_chunk_validation_status": "VALID", 
            "current_chunk_translated_text": cleaned_text 
        }
    else:
        logger.warning(f"Validation for Chunk {chunk_idx + 1}: FAILED (Markdown Block Detected) (Retry {retry_count + 1})")
        if retry_count >= MAX_TRANSLATION_RETRIES:
            logger.warning(f"Max retries ({MAX_TRANSLATION_RETRIES}) reached for chunk {chunk_idx + 1} due to markdown blocks.")
            return {"current_chunk_validation_status": "INVALID_MAX_RETRIES_REACHED"}
        else:
            return {
                "current_chunk_validation_status": "INVALID_NEEDS_RETRY",
                "current_chunk_retry_count": retry_count + 1
            }

def decide_after_validation(state: AgentState) -> str:
    """Determines the next step based on the translation validation status of the current chunk."""
    status = state.get('current_chunk_validation_status')
    chunk_idx = state.get('current_chunk_index', 0)
    if status == "VALID":
        return "proceed_to_aggregate"
    elif status == "INVALID_NEEDS_RETRY":
        return "retry_chunk_translation"
    elif status == "INVALID_MAX_RETRIES_REACHED":
        logger.warning(f"Chunk {chunk_idx + 1} translation failed after max retries (markdown block issue). Using original text as placeholder.")
        return "proceed_to_aggregate_with_placeholder" 
    else: 
        logger.error(f"Error: Unknown validation status '{status}' for chunk {chunk_idx + 1}. Ending process.")
        return END 

def aggregate_translation_node(state: AgentState) -> dict:
    """Aggregates the validated (or placeholder) translated text for the current chunk and updates the state."""
    chunk_idx = state.get('current_chunk_index', 0)
    logger.info(f"Aggregating translation for chunk {chunk_idx + 1}...")
    translated_chunks_list = state.get('translated_chunks_list', [])
    text_to_append_for_aggregation = state.get('current_chunk_translated_text') 
    validation_status = state.get('current_chunk_validation_status')

    if validation_status == "INVALID_MAX_RETRIES_REACHED":
        original_text = state.get('current_chunk_original_text', "[ERROR: Placeholder - Original Text Missing]")
        text_to_append_for_aggregation = f"[TRANSLATION FAILED (MARKDOWN BLOCK) - ORIGINAL TEXT BELOW]\n{original_text}"
        logger.warning(f"Using original text as placeholder for chunk {chunk_idx + 1} due to validation failure.")
    elif validation_status == "VALID":
        if text_to_append_for_aggregation is None: 
             original_text = state.get('current_chunk_original_text', "[ERROR: Placeholder - Original Text Missing]")
             text_to_append_for_aggregation = f"[ERROR: VALID BUT TEXT MISSING - ORIGINAL TEXT BELOW]\n{original_text}"
             logger.warning(f"Chunk {chunk_idx + 1} was VALID but translated text is None. Appending placeholder.")
    else: 
        original_text = state.get('current_chunk_original_text', "[ERROR: Placeholder - Original Text Missing]")
        text_to_append_for_aggregation = f"[ERROR: UNEXPECTED VALIDATION STATUS ({validation_status}) - ORIGINAL TEXT BELOW]\n{original_text}"
        logger.info(f"Aggregating translation for chunk {chunk_idx + 1}. Status: {validation_status}")
    
    translated_chunks_list.append(text_to_append_for_aggregation)
    new_index = chunk_idx + 1
    return {
        "translated_chunks_list": translated_chunks_list,
        "current_chunk_index": new_index,
        "current_chunk_retry_count": 0 
    }

def should_translate_more_chunks(state: AgentState) -> str: 
    """Checks if there are more subtitle chunks to translate.""" 
    current_chunk_index = state.get('current_chunk_index', 0)
    sub_chunks_list = state.get('sub_chunks_list')
    if sub_chunks_list and current_chunk_index < len(sub_chunks_list):
        logger.info(f"Translating chunk {current_chunk_index + 1}/{len(sub_chunks_list)}")
        return "translate_next_chunk" 
    else:
        return "finish_translation" 

def finalize_translation_node(state: AgentState) -> dict:
    """Parses aggregated translated text, reconstructs the subtitle list, and saves the final translated SRT file."""
    logger.info("Finalizing translation...")
    translated_chunks_list = state.get('translated_chunks_list')
    sub_list = state.get('sub_list') 
    original_srt_path = state.get('original_srt_path')
    
    if not sub_list: 
        logger.warning("No original subtitles to finalize.")
        return {"messages": [SystemMessage(content="No subtitles to finalize.")]}
    if not translated_chunks_list : 
         logger.warning("No translated chunks to finalize. Using original subtitles.")
    
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
            logger.warning(f"Warning: Finalize - Could not parse line: '{line}'")

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
    logger.info(f"Successfully parsed SRT. Number of entries: {len(sub_list)}")
    logger.info(f"Translated SRT saved to: {final_srt_path}")
    return {
        "translated_sub_list": translated_sub_list_output, "final_srt_path": final_srt_path,
        "messages": [SystemMessage(content=f"Translation complete. Final SRT saved to {final_srt_path}")]
    }

# Graph definition
graph = StateGraph(AgentState)

# Add new nodes for the refined input flow
graph.add_node('get_video_link', get_video_link_node)
graph.add_node('display_available_languages', display_available_languages_node)
graph.add_node('get_language_choices', get_language_choices_node)

graph.add_node('getsub', get_sub_node)
extraction_tool_node = ToolNode(tools=extraction_tools)
graph.add_node('extraction_tools', extraction_tool_node)

graph.add_node('prepare_translation', prepare_translation_node)
graph.add_node('generate_translation_context', generate_translation_context_node)
graph.add_node('translate_current_chunk', translate_current_chunk_node)
graph.add_node('validate_translation_format', validate_translation_format_node) 
graph.add_node('aggregate_translation', aggregate_translation_node)
graph.add_node('finalize_translation', finalize_translation_node)

# Define edges for the new flow
graph.add_edge(START, 'get_video_link')
graph.add_edge('get_video_link', 'display_available_languages')
graph.add_conditional_edges(
    'display_available_languages',
    decide_after_displaying_languages,
    {
        "get_language_choices": 'get_language_choices',
        END: END
    }
)
graph.add_edge('get_language_choices', 'getsub')

# Edges for subtitle processing flow
graph.add_conditional_edges(
    'getsub', 
    should_continue_extraction,
    {
        "continue_extraction": 'extraction_tools', 
        "start_translation": 'prepare_translation', 
        "end_process": END
    }
)
graph.add_edge('extraction_tools', 'getsub') # Loop back to get_sub_node to process tool output
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

# Main execution block to run the agent.
if __name__ == '__main__':
    config = {"recursion_limit": 250} 
    initial_state = {} 
    for event in app.stream(initial_state, config=config):
        for k, v in event.items():
            if k != "__end__":
                logger.info(f"Output from node: {k}")
                if 'messages' in v and v['messages']:
                    last_message = v['messages'][-1]
                    logger.info(f"  Last Msg: {last_message.type}, Content (first 100 chars): {str(last_message.content)[:100]}...")
                if 'original_srt_path' in v and v['original_srt_path']:
                    logger.info(f"  Original SRT: {v['original_srt_path']}")
                if 'final_srt_path' in v and v['final_srt_path']:
                    logger.info(f"  Final SRT: {v['final_srt_path']}")
                if 'sub_chunks_list' in v and v['sub_chunks_list'] is not None:
                    chunk_len = len(v['sub_chunks_list']) if v['sub_chunks_list'] else 0
                    idx = v.get('current_chunk_index',0)
                    retry = v.get('current_chunk_retry_count',0)
                    status = v.get('current_chunk_validation_status','')
                    logger.info(f"  Chunk Prog: {idx}/{chunk_len}, Retry: {retry}, Status: {status}")
                logger.info("---")
        logger.info("##################################################")
