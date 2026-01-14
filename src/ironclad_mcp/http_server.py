"""
Ironclad MCP HTTP Server
Streamable HTTP transport for multi-user deployment
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

from mcp.server import Server
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

# Import MCP tools from server.py
from .server import create_server

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/tmp/ironclad-mcp-http.log')
    ]
)
logger = logging.getLogger(__name__)


class IroncladMCPHTTPServer:
    """HTTP/SSE server for Ironclad MCP"""
    
    def __init__(self):
        self.app = Starlette(
            routes=[
                Route("/sse", self.handle_sse, methods=["GET"]),
                Route("/health", self.handle_health, methods=["GET"]),
            ]
        )
    
    async def handle_health(self, request: Request) -> Response:
        """Health check endpoint"""
        return Response(
            content=json.dumps({
                "status": "healthy",
                "service": "ironclad-mcp",
                "version": "1.0.0"
            }),
            media_type="application/json"
        )
    
    async def handle_sse(self, request: Request) -> Response:
        """Handle SSE connection for MCP"""
        # Get user email from headers (required for user attribution)
        user_email = request.headers.get("X-User-Email")
        if not user_email:
            logger.error("Missing X-User-Email header")
            return Response(
                content="Missing X-User-Email header",
                status_code=400
            )
        
        logger.info(f"New SSE connection from user: {user_email}")
        
        # Set user email in environment for this request
        os.environ["IRONCLAD_USER_EMAIL"] = user_email
        
        # Create MCP server instance
        server = create_server()
        
        # Create SSE transport
        sse = SseServerTransport("/messages")
        
        async def handle_connection(read_stream, write_stream):
            """Handle the MCP connection"""
            try:
                async with server.run(
                    read_stream=read_stream,
                    write_stream=write_stream,
                    initialization_options=server._initialization_options or {}
                ):
                    logger.info(f"MCP server running for user: {user_email}")
                    # Keep connection alive
                    await asyncio.Event().wait()
            except Exception as e:
                logger.error(f"Error in MCP connection for {user_email}: {e}", exc_info=True)
                raise
        
        # Handle the SSE connection
        return await sse.handle_sse(
            request=request,
            handle_connection=handle_connection
        )


def create_app() -> Starlette:
    """Create and configure the Starlette application"""
    server = IroncladMCPHTTPServer()
    return server.app


# For running with uvicorn
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting Ironclad MCP HTTP server on {host}:{port}")
    
    # Verify required environment variables
    required_vars = [
        "GCP_PROJECT_ID",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "IRONCLAD_BASE_URL"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
    
    logger.info("Environment configuration validated")
    logger.info(f"GCP Project: {os.getenv('GCP_PROJECT_ID')}")
    logger.info(f"Ironclad URL: {os.getenv('IRONCLAD_BASE_URL')}")
    
    # Run the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
