# Deployment Checklist

Use this checklist to ensure a smooth production deployment.

---

## Pre-Deployment

### Environment Configuration

- [ ] Create production `.env` file (never commit to git)
- [ ] Generate strong LiveKit API key and secret
- [ ] Obtain production Gemini API key with billing enabled
- [ ] Obtain production CodeVoice API key
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR` for production
- [ ] Configure proper `SESSION_TIMEOUT` value
- [ ] Review all environment variables

### Security

- [ ] Configure CORS `allow_origins` for production domains only
- [ ] Enable HTTPS for all endpoints
- [ ] Set up SSL certificates (Let's Encrypt or commercial)
- [ ] Implement rate limiting
- [ ] Add authentication/authorization system
- [ ] Sanitize all user inputs
- [ ] Implement CSRF protection
- [ ] Set secure HTTP headers
- [ ] Remove debug endpoints
- [ ] Disable detailed error messages in production

### Infrastructure

- [ ] Choose hosting platform (AWS, GCP, Azure, DigitalOcean, etc.)
- [ ] Provision servers with adequate resources
- [ ] Set up domain names and DNS records
- [ ] Configure load balancer (if needed)
- [ ] Set up CDN for frontend assets
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerting
- [ ] Configure backup strategy
- [ ] Plan disaster recovery

---

## LiveKit Configuration

### LiveKit Server

- [ ] Deploy LiveKit server (self-hosted or LiveKit Cloud)
- [ ] Configure TURN/STUN servers for NAT traversal
- [ ] Set up proper SSL certificates for LiveKit
- [ ] Configure WebSocket connection (wss:// not ws://)
- [ ] Test LiveKit connectivity from target regions
- [ ] Configure room cleanup policies
- [ ] Set up LiveKit monitoring
- [ ] Configure bandwidth limits

### Redis

- [ ] Deploy Redis instance (managed or self-hosted)
- [ ] Configure Redis authentication
- [ ] Set up Redis persistence
- [ ] Configure Redis memory limits
- [ ] Test Redis connectivity
- [ ] Set up Redis monitoring

---

## Backend Deployment

### Database (Future Enhancement)

- [ ] Choose database (PostgreSQL recommended)
- [ ] Set up database server
- [ ] Create database and user
- [ ] Run migrations
- [ ] Configure connection pooling
- [ ] Set up database backups
- [ ] Test database connectivity

### Application

- [ ] Update `docker-compose.yml` for production
- [ ] Remove development overrides
- [ ] Configure proper logging (JSON format)
- [ ] Set up log aggregation (ELK, Datadog, etc.)
- [ ] Configure health check endpoints
- [ ] Set up automated testing
- [ ] Run load testing
- [ ] Test all API endpoints
- [ ] Verify external API connectivity (Gemini, CodeVoice)

### Performance

- [ ] Configure appropriate number of workers
- [ ] Set up connection pooling
- [ ] Configure timeouts appropriately
- [ ] Implement caching strategy
- [ ] Optimize database queries
- [ ] Set up performance monitoring
- [ ] Test under expected load
- [ ] Configure auto-scaling (if applicable)

---

## Frontend Deployment

### Build

- [ ] Set production environment variables
- [ ] Run production build (`npm run build`)
- [ ] Verify build output
- [ ] Test production build locally
- [ ] Optimize bundle size
- [ ] Configure asset caching
- [ ] Set up CDN distribution

### Nginx Configuration

- [ ] Update nginx.conf for production
- [ ] Configure SSL/TLS
- [ ] Set up HTTP/2
- [ ] Configure gzip compression
- [ ] Set up proper caching headers
- [ ] Configure security headers
- [ ] Set up rate limiting
- [ ] Test nginx configuration

### Browser Compatibility

- [ ] Test on Chrome (primary)
- [ ] Test on Firefox
- [ ] Test on Safari
- [ ] Test on Edge
- [ ] Test on mobile browsers
- [ ] Verify Web Speech API support
- [ ] Test microphone permissions flow

---

## Testing

### Functional Testing

- [ ] Test session creation
- [ ] Test voice recognition (STT)
- [ ] Test LLM response generation
- [ ] Test TTS audio generation
- [ ] Test audio playback
- [ ] Test conversation history
- [ ] Test session cleanup
- [ ] Test error handling
- [ ] Test reconnection logic

### Integration Testing

- [ ] Test LiveKit connection
- [ ] Test Gemini API integration
- [ ] Test CodeVoice TTS integration
- [ ] Test end-to-end conversation flow
- [ ] Test concurrent sessions
- [ ] Test network failures
- [ ] Test API rate limits

### Performance Testing

- [ ] Load test backend API
- [ ] Load test LiveKit server
- [ ] Test concurrent conversations
- [ ] Measure response times
- [ ] Test under peak load
- [ ] Identify bottlenecks
- [ ] Optimize slow endpoints

### Security Testing

- [ ] Run vulnerability scans
- [ ] Test for XSS vulnerabilities
- [ ] Test for CSRF vulnerabilities
- [ ] Test for SQL injection
- [ ] Test authentication bypass
- [ ] Test API key exposure
- [ ] Review access controls
- [ ] Test input validation

---

## Monitoring & Observability

### Logging

- [ ] Configure structured logging (JSON)
- [ ] Set up log aggregation
- [ ] Configure log retention policy
- [ ] Set up log search capabilities
- [ ] Create log dashboards
- [ ] Configure log alerts

### Metrics

- [ ] Set up metrics collection (Prometheus)
- [ ] Create Grafana dashboards
- [ ] Monitor API response times
- [ ] Monitor error rates
- [ ] Monitor active sessions
- [ ] Monitor resource usage (CPU, memory, disk)
- [ ] Monitor external API latency
- [ ] Monitor LiveKit connections

### Alerts

- [ ] Configure alert thresholds
- [ ] Set up alert notifications (email, Slack, PagerDuty)
- [ ] Test alert delivery
- [ ] Create runbooks for common alerts
- [ ] Set up on-call rotation

---

## Documentation

### Internal

- [ ] Update deployment documentation
- [ ] Create operations runbook
- [ ] Document troubleshooting procedures
- [ ] Create incident response plan
- [ ] Document scaling procedures
- [ ] Document backup/restore procedures

### External

- [ ] Update user documentation
- [ ] Create API documentation
- [ ] Write troubleshooting guide
- [ ] Create FAQ
- [ ] Document known limitations
- [ ] Create video tutorials (optional)

---

## Go-Live Preparation

### Final Checks

- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Security audit completed
- [ ] Monitoring in place
- [ ] Alerts configured
- [ ] Documentation updated
- [ ] Team trained on operations
- [ ] Support team briefed
- [ ] Rollback plan ready

### Rollback Plan

- [ ] Document rollback procedure
- [ ] Test rollback process
- [ ] Keep previous version available
- [ ] Plan maintenance window
- [ ] Prepare communication template

### Communication

- [ ] Announce deployment schedule
- [ ] Prepare status page update
- [ ] Create user communication
- [ ] Set up support channels
- [ ] Brief customer support team

---

## Post-Deployment

### Immediate (0-24 hours)

- [ ] Monitor error rates closely
- [ ] Monitor response times
- [ ] Check all service health
- [ ] Verify LiveKit connections
- [ ] Verify external API connectivity
- [ ] Monitor resource usage
- [ ] Check logs for errors
- [ ] Respond to user feedback

### Short-term (1-7 days)

- [ ] Review performance metrics
- [ ] Analyze error patterns
- [ ] Optimize slow endpoints
- [ ] Address user-reported issues
- [ ] Monitor usage patterns
- [ ] Review costs
- [ ] Update documentation

### Long-term (Ongoing)

- [ ] Regular security audits
- [ ] Performance optimization
- [ ] Feature enhancements
- [ ] User feedback integration
- [ ] Capacity planning
- [ ] Cost optimization
- [ ] Technology updates
- [ ] Backup testing

---

## Production Configuration Example

### Production `.env` File

```env
# LiveKit Configuration
LIVEKIT_API_KEY=<production-key>
LIVEKIT_API_SECRET=<production-secret>
LIVEKIT_URL=wss://livekit.yourdomain.com

# LLM Configuration
GEMINI_API_KEY=<production-key>
GEMINI_MODEL=gemini-pro
GEMINI_MAX_TOKENS=2048
GEMINI_TEMPERATURE=0.7

# CodeVoice TTS Configuration
CODEVOICE_API_KEY=<production-key>
CODEVOICE_BASE_URL=https://voices.codelessai.in
CODEVOICE_VOICE=Ryan
CODEVOICE_POLL_INTERVAL=2
CODEVOICE_MAX_POLLS=60

# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=WARNING
ENVIRONMENT=production

# Session Configuration
SESSION_TIMEOUT=1800
MAX_CONVERSATION_HISTORY=50
```

### Production Docker Compose Modifications

```yaml
# Remove development overrides
# Add resource limits
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
    
  frontend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

---

## Useful Commands

### Deployment

```bash
# Build and start
docker compose -f docker-compose.yml up -d --build

# View logs
docker compose logs -f --tail=100

# Check service health
docker compose ps

# Restart service
docker compose restart backend

# Update service
docker compose pull backend
docker compose up -d backend

# Rollback
docker compose down
# Update docker-compose.yml to previous version
docker compose up -d
```

### Monitoring

```bash
# Check backend health
curl https://api.yourdomain.com/health

# Check API status
curl https://api.yourdomain.com/api/status

# View recent logs
docker compose logs --tail=50 backend

# Check resource usage
docker stats
```

### Maintenance

```bash
# Stop all services
docker compose down

# Clean up
docker system prune -a

# Backup volumes
docker run --rm -v redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .

# Restore volumes
docker run --rm -v redis-data:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /data
```

---

## Emergency Procedures

### Service Down

1. Check service status: `docker compose ps`
2. View logs: `docker compose logs service-name`
3. Restart service: `docker compose restart service-name`
4. If persistent, rollback to previous version

### High Error Rate

1. Check logs for error patterns
2. Verify external API connectivity
3. Check resource usage
4. Scale up if needed
5. Enable detailed logging temporarily

### Performance Degradation

1. Check resource usage: `docker stats`
2. Review slow queries/logs
3. Check external API latency
4. Scale horizontally if possible
5. Enable caching if not active

### Security Incident

1. Isolate affected services
2. Review logs for attack patterns
3. Rotate API keys
4. Patch vulnerabilities
5. Notify affected users
6. Document incident

---

## Success Criteria

Your deployment is successful when:

- ✅ All services running healthy for 24+ hours
- ✅ Error rate < 1%
- ✅ API response times within targets
- ✅ User feedback is positive
- ✅ No critical security issues
- ✅ Monitoring and alerts working
- ✅ Team confident in operations
- ✅ Documentation is complete and accurate

---

**Remember: Production deployment is not the end, it's the beginning of continuous improvement!**
