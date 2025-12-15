"""
Self-Evolution Analysis Daemon
Periodically analyzes patterns and generates optimization recommendations
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


class AnalysisDaemon:
    """Background daemon for continuous pattern analysis"""
    
    def __init__(self):
        self.evolution_service_url = os.getenv('EVOLUTION_SERVICE_URL', 'http://self-evolution:5007')
        self.analysis_interval = int(os.getenv('ANALYSIS_INTERVAL', 3600))  # 1 hour default
        self.auto_apply = os.getenv('AUTO_APPLY_OPTIMIZATIONS', 'false').lower() == 'true'
        self.running = False
        logger.info(f"Analysis daemon initialized with {self.analysis_interval}s interval")
        logger.info(f"Auto-apply optimizations: {self.auto_apply}")
    
    async def run(self):
        """Main daemon loop"""
        self.running = True
        logger.info("Starting self-evolution analysis daemon...")
        
        while self.running:
            try:
                await self.perform_analysis()
                await asyncio.sleep(self.analysis_interval)
            except KeyboardInterrupt:
                logger.info("Daemon shutdown requested")
                self.running = False
            except Exception as e:
                logger.error(f"Error in analysis loop: {e}")
                await asyncio.sleep(60)  # Brief pause before retry
    
    async def perform_analysis(self):
        """Perform pattern analysis and generate recommendations"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                # Trigger analysis
                response = await client.post(f"{self.evolution_service_url}/analyze")
                
                if response.status_code == 200:
                    result = response.json()
                    patterns_analyzed = result.get('patterns_analyzed', 0)
                    recommendations_count = result.get('recommendations_generated', 0)
                    
                    logger.info(f"Analysis complete: {patterns_analyzed} patterns, "
                              f"{recommendations_count} recommendations")
                    
                    if recommendations_count > 0 and self.auto_apply:
                        await self.auto_apply_recommendations(result.get('recommendations', []))
                else:
                    logger.error(f"Analysis failed with status {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Failed to perform analysis: {e}")
    
    async def auto_apply_recommendations(self, recommendations):
        """Auto-apply high-priority recommendations"""
        logger.info(f"Auto-applying {len(recommendations)} recommendations")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            for rec in recommendations:
                # Only auto-apply high priority recommendations
                if rec.get('priority') in ['high', 'critical']:
                    rec_id = rec.get('id')
                    try:
                        response = await client.post(
                            f"{self.evolution_service_url}/apply-optimization/{rec_id}"
                        )
                        
                        if response.status_code == 200:
                            logger.info(f"Applied optimization {rec_id}: {rec.get('description')}")
                        else:
                            logger.warning(f"Failed to apply optimization {rec_id}")
                            
                    except Exception as e:
                        logger.error(f"Error applying optimization {rec_id}: {e}")


async def main():
    daemon = AnalysisDaemon()
    await daemon.run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Daemon stopped")
        sys.exit(0)
