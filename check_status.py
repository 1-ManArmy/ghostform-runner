#!/usr/bin/env python3
import argparse
import json
import os
from pin_manager import get_pin_manager

def main():
    parser = argparse.ArgumentParser(description="View PIN testing status")
    parser.add_argument('--confirmation', type=str, default="1234567890", help='Confirmation number')
    args = parser.parse_args()
    
    pm = get_pin_manager(args.confirmation)
    stats = pm.get_stats()
    
    print("=" * 60)
    print(f"PIN TESTING STATUS FOR: {args.confirmation}")
    print("=" * 60)
    print(f"📊 Total PINs tried: {stats['total_pins_tried']:,}")
    print(f"🎯 Total attempts: {stats['total_attempts']:,}")
    print(f"🤖 Agents used: {stats['agents_used']}")
    print(f"📋 Remaining PINs: {stats['remaining_pins']:,}")
    print(f"✅ Success PIN: {stats['success_pin'] or 'Not found yet'}")
    print(f"📁 Data file: {pm.data_file}")
    print(f"📋 Log file: {pm.log_file}")
    
    if stats['success_pin']:
        print("\n🎉 SUCCESS! PIN has been found!")
    else:
        completion = (stats['total_pins_tried'] / 10000) * 100
        print(f"\n📈 Progress: {completion:.2f}% of all possible PINs tested")
    
    print("\n" + "=" * 60)
    
    # Show recent agents
    if pm.data.get('agents_used'):
        print("📋 Recent agents:")
        for agent in pm.data['agents_used'][-5:]:  # Last 5 agents
            print(f"  • {agent['agent']}: {len(agent['pins'])} PINs at {agent['timestamp']}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
