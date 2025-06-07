# -*- coding: utf-8 -*-

import time
import logging

# Configure logging
logger = logging.getLogger(__name__)
if not logger.hasHandlers():  # Avoid adding multiple handlers if this module is reloaded
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO) # Default level, can be adjusted (e.g., logging.DEBUG for more verbosity)

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

# ==============================================================================
# ---                           配置区域 (Configuration)                      ---
# ==============================================================================

# 1. 目标视频ID
VIDEO_ID = 'HvaUdCTMkkk'

# 2. 语言优先级列表 (会从左到右依次尝试)
#    优先获取 'en-US' (通常是手动创建的高质量字幕)
#    如果失败，则回退到 'en' (通常是YouTube自动生成的字幕)
LANGUAGE_PRIORITY = ['en-US', 'en']

# 3. 代理设置
#    如果你在使用Clash或其他代理工具，请设置为True
USE_PROXY = True
#    Clash for Windows/macOS 默认的HTTP代理端口通常是 7890
#    如果你的端口不同，请修改下面的 '7890'
PROXY_CONFIG = {
   'http': 'http://127.0.0.1:7890',
   'https': 'http://127.0.0.1:7890',
}

# 4. 自动重试设置
MAX_RETRIES = 5              # 最大重试次数
RETRY_DELAY_SECONDS = 3      # 每次重试之间的等待时间（秒）

# ==============================================================================
# ---                           核心功能函数                                ---
# ==============================================================================

def get_transcript_robustly(video_id, lang_priority, use_proxy, proxy_config, max_retries, retry_delay):
    """
    一个健壮的YouTube字幕获取函数。
    集成了代理支持、语言优先级选择和自动重试机制。
    """
    proxies = proxy_config if use_proxy else None
    
    # 步骤 1: 获取可用字幕列表 (如果启用，则通过代理)
    try:
        logger.info("Attempting to fetch the list of available transcripts...")
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
    except TranscriptsDisabled:
        logger.error(f"Transcripts are disabled for video '{video_id}'.")
        return None
    except NoTranscriptFound:
        logger.error(f"No transcripts found for video '{video_id}'.")
        return None
    except Exception as e:
        logger.error(f"Unknown error occurred while fetching transcript list for video '{video_id}': {e}", exc_info=True)
        return None

    # 步骤 2: 根据优先级列表，查找最佳可用字幕
    target_transcript = None
    for lang_code in lang_priority:
        target_transcript = transcript_list.find_transcript([lang_code])
        if target_transcript:
            logger.info(f"Found best available transcript -> Language code: '{target_transcript.language_code}', Is auto-generated: {target_transcript.is_generated}")
            break
            
    if not target_transcript:
        available_langs = [t.language_code for t in transcript_list]
        logger.error(f"Could not find any desired language from {lang_priority} in available transcripts: {available_langs}.")
        return None

    # 步骤 3: 使用重试循环来获取选定的字幕
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempt {attempt + 1}/{max_retries} to fetch transcript '{target_transcript.language_code}'...")
            # 注意：fetch() 方法不接受代理参数，代理在创建Transcript对象时已经设置好
            # 这里我们直接调用 get_transcript 来获取最终数据，它会处理代理
            transcript_data = YouTubeTranscriptApi.get_transcript(
                video_id,
                languages=[target_transcript.language_code],
                proxies=proxies
            )
            logger.info("Successfully fetched transcript content!")
            return transcript_data
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries} failed for transcript '{target_transcript.language_code}': {e}", exc_info=True)
            if attempt + 1 < max_retries:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Maximum retry attempts reached. Fetching failed.")
                return None
    return None

# ==============================================================================
# ---                           主程序入口                                  ---
# ==============================================================================

if __name__ == "__main__":
    logger.info("--- YouTube Robust Transcript Fetcher Script ---")
    logger.info(f"Video ID: {VIDEO_ID}")
    logger.info(f"Language priority: {LANGUAGE_PRIORITY}")
    proxy_status_log = f"Yes, Address: {PROXY_CONFIG['http']}" if USE_PROXY else "No"
    logger.info(f"Using proxy: {proxy_status_log}")
    logger.info(f"Max retries: {MAX_RETRIES}")
    logger.info("-" * 35)

    final_transcript = get_transcript_robustly(
        video_id=VIDEO_ID,
        lang_priority=LANGUAGE_PRIORITY,
        use_proxy=USE_PROXY,
        proxy_config=PROXY_CONFIG,
        max_retries=MAX_RETRIES,
        retry_delay=RETRY_DELAY_SECONDS
    )

    if final_transcript:
        logger.info("--- Transcript fetched successfully! ---")
        logger.info(f"Fetched {len(final_transcript)} subtitle entries.")
        logger.info("Subtitle content preview (first 3 entries):")
        for i, line in enumerate(final_transcript[:3]):
            start_time = f"{line['start']:.2f}".rjust(7)
            logger.info(f"  [{i+1}] Start time: {start_time}s | Content: {line['text']}")
    else:
        logger.info("--- Task finished: Failed to fetch subtitles. ---")