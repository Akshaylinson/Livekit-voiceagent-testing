#!/bin/bash

# Stop all services
echo "🛑 Stopping AI Voice Agent services..."

docker compose down

echo ""
echo "✅ All services stopped."
echo ""
echo "💡 To remove volumes as well, run: docker compose down -v"
