"""
Health Monitor Daemon
Continuously monitors services and triggers auto-healing
"""

import asyncio
import httpx
import logging
import os
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MonitoringDaemon:
    """Background daemon for continuous health monitoring"""
    
    def __init__(self):
        self.health_monitor_url = os.getenv('HEALTH_MONITOR_URL', 'http://health-monitor:5006')
        self.check_interval = int(os.getenv('DAEMON_CHECK_INTERVAL', 30))
        self.running = False
        logger.info(f"Monitoring daemon initialized with {self.check_interval}s interval")
    
    async def run(self):
        """Main daemon loop"""
        self.running = True
        logger.info("Starting health monitoring daemon...")
        
        while self.running:
            try:
                await self.perform_health_check()
                await asyncio.sleep(self.check_interval)
            except KeyboardInterrupt:
                logger.info("Daemon shutdown requested")
                self.running = False
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(5)  # Brief pause before retry
    
    async def perform_health_check(self):
        """Perform health check on all services"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(f"{self.health_monitor_url}/check-services")
                
                if response.status_code == 200:
                    results = response.json()
                    unhealthy = [
                        name for name, status in results.items() 
                        if status.get('status') != 'healthy'
                    ]
                    
                    if unhealthy:
                        logger.warning(f"Unhealthy services detected: {', '.join(unhealthy)}")
                    else:
                        logger.info("All services healthy")
                else:
                    logger.error(f"Health check failed with status {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Failed to perform health check: {e}")


async def main():
    daemon = MonitoringDaemon()
    await daemon.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Daemon stopped")
        sys.exit(0)
