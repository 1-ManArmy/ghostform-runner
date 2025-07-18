#!/bin/bash
# Git Bash Launcher for Real PIN Hunter - Booking ID: 6160911170
# Optimized for stealth mode and proxy automation

# Colors for Git Bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Configuration
PYTHON_PATH="C:/Users/HP/Pablo_Agent/ghostform-runner/venv/Scripts/python.exe"
SCRIPT_PATH="real_pin_hunter_6160911170.py"
BOOKING_ID="6160911170"

# Function to display banner
show_banner() {
    clear
    echo -e "${CYAN}${BOLD}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                              ║"
    echo "║                    🎯 STEALTH PIN HUNTER - GIT BASH 🎯                      ║"
    echo "║                                                                              ║"
    echo "║  Real Booking ID: 6160911170                                                ║"
    echo "║  Mode: Stealth + Proxy Automation                                          ║"
    echo "║  Environment: Git Bash (Optimized)                                         ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to show deployment menu
show_menu() {
    echo -e "${YELLOW}${BOLD}🚀 DEPLOYMENT OPTIONS:${NC}"
    echo ""
    echo -e "${WHITE}1.${NC} ${GREEN}🔍 Single Agent${NC} - Stealth test (10 attempts)"
    echo -e "${WHITE}2.${NC} ${BLUE}👥 Small Squad${NC} - 3 agents = 30 attempts"
    echo -e "${WHITE}3.${NC} ${CYAN}🚀 Medium Force${NC} - 5 agents = 50 attempts"
    echo -e "${WHITE}4.${NC} ${YELLOW}💪 Strong Army${NC} - 10 agents = 100 attempts"
    echo -e "${WHITE}5.${NC} ${RED}🔥 MASSIVE ARMY${NC} - 20 agents = 200 attempts"
    echo -e "${WHITE}6.${NC} ${CYAN}📊 Monitor Progress${NC} - Real-time tracking"
    echo -e "${WHITE}7.${NC} ${GREEN}🧪 System Check${NC} - Verify setup"
    echo -e "${WHITE}8.${NC} ${RED}🚪 Exit${NC}"
    echo ""
    echo -e "${BOLD}Enter your choice (1-8): ${NC}"
}

# Function to deploy agents
deploy_agents() {
    local count=$1
    local name=$2
    
    echo -e "${GREEN}${BOLD}🚀 Deploying ${name} (${count} agents)...${NC}"
    echo -e "${YELLOW}⚠️  Running in stealth mode with proxy automation${NC}"
    
    for i in $(seq 1 $count); do
        echo -e "${CYAN}Starting Agent ${i}/${count}...${NC}"
        "$PYTHON_PATH" "$SCRIPT_PATH" &
        sleep 1  # Small delay between agents
    done
    
    echo -e "${GREEN}✅ ${count} agents deployed successfully!${NC}"
    echo -e "${YELLOW}💡 Each agent will try 10 PINs, then return home${NC}"
    echo -e "${BLUE}📊 Monitor with: ./launch_real_hunter_bash.sh (option 6)${NC}"
}

# Function to check system
check_system() {
    echo -e "${CYAN}${BOLD}🧪 SYSTEM CHECK${NC}"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    
    # Check Python
    if [ -f "$PYTHON_PATH" ]; then
        echo -e "${GREEN}✅ Python found: $PYTHON_PATH${NC}"
    else
        echo -e "${RED}❌ Python not found: $PYTHON_PATH${NC}"
        return 1
    fi
    
    # Check script
    if [ -f "$SCRIPT_PATH" ]; then
        echo -e "${GREEN}✅ Hunter script found: $SCRIPT_PATH${NC}"
    else
        echo -e "${RED}❌ Hunter script not found: $SCRIPT_PATH${NC}"
        return 1
    fi
    
    # Check proxy credentials
    if grep -q "phantom1_rOHk6" "$SCRIPT_PATH"; then
        echo -e "${GREEN}✅ Proxy credentials updated${NC}"
    else
        echo -e "${RED}❌ Proxy credentials not updated${NC}"
        return 1
    fi
    
    echo -e "${GREEN}✅ System ready for stealth operation!${NC}"
    echo "═══════════════════════════════════════════════════════════════════════════════"
}

# Function to monitor progress
monitor_progress() {
    echo -e "${CYAN}${BOLD}📊 STARTING REAL-TIME MONITOR...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop monitoring${NC}"
    "$PYTHON_PATH" monitor_real_hunt.py
}

# Function to show current status
show_status() {
    echo -e "${CYAN}${BOLD}📊 CURRENT STATUS${NC}"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    
    # Check for success
    if [ -f "REAL_SUCCESS_${BOOKING_ID}.json" ]; then
        echo -e "${GREEN}${BOLD}🎉 SUCCESS FOUND!${NC}"
        cat "REAL_SUCCESS_${BOOKING_ID}.json"
    else
        echo -e "${YELLOW}⏳ Hunt in progress...${NC}"
    fi
    
    # Check log file
    if [ -f "real_hunt_log_${BOOKING_ID}.txt" ]; then
        local attempts
        local progress
        attempts=$(wc -l < "real_hunt_log_${BOOKING_ID}.txt")
        progress=$(echo "scale=2; $attempts / 100" | bc 2>/dev/null || echo "0")
        echo -e "${CYAN}📋 Total attempts: $attempts${NC}"
        echo -e "${CYAN}📊 Progress: ${progress}%${NC}"
        echo ""
        echo -e "${YELLOW}📋 Latest attempts:${NC}"
        tail -5 "real_hunt_log_${BOOKING_ID}.txt"
    else
        echo -e "${GRAY}📋 No attempts yet${NC}"
    fi
    
    echo "═══════════════════════════════════════════════════════════════════════════════"
}

# Main menu loop
main() {
    while true; do
        show_banner
        show_status
        show_menu
        
        read -r choice
        
        case $choice in
            1)
                deploy_agents 1 "Single Agent (Stealth Test)"
                ;;
            2)
                deploy_agents 3 "Small Squad"
                ;;
            3)
                deploy_agents 5 "Medium Force"
                ;;
            4)
                deploy_agents 10 "Strong Army"
                ;;
            5)
                echo -e "${RED}${BOLD}🔥 MASSIVE ARMY DEPLOYMENT${NC}"
                echo -e "${YELLOW}⚠️  This will deploy 20 agents simultaneously!${NC}"
                echo -e "${YELLOW}Continue? (y/N): ${NC}"
                read -r confirm
                if [[ $confirm =~ ^[Yy]$ ]]; then
                    deploy_agents 20 "MASSIVE ARMY"
                else
                    echo -e "${BLUE}Deployment cancelled${NC}"
                fi
                ;;
            6)
                monitor_progress
                ;;
            7)
                check_system
                ;;
            8)
                echo -e "${GREEN}${BOLD}👋 Happy hunting, Boss!${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice. Please try again.${NC}"
                ;;
        esac
        
        echo ""
        echo -e "${BLUE}Press Enter to continue...${NC}"
        read -r
    done
}

# Run main function
main
