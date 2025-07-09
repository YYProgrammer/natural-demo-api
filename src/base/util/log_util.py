import logging

# 检查是否已经配置过日志
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s %(name)s - %(message)s")
    logging.info("Logging configured")

logger = logging
