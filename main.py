import MetaTrader5 as mt5
import requests
import time

# Replace with your Pepperstone API credentials
PEPPERSTONE_API_KEY = 'your_api_key_here'
PEPPERSTONE_ACCOUNT_ID = 'your_account_id_here'
PEPPERSTONE_API_URL = 'https://api.pepperstone.com/v1/accounts'

# Initialize MetaTrader 5
if not mt5.initialize():
    print("Failed to initialize MetaTrader 5")
    exit()

# Constants
INITIAL_BALANCE = 5000  # Example balance (replace with actual balance)
MAX_DRAWDOWN_OVERALL = 0.20  # 20% overall max drawdown
MAX_DRAWDOWN_DAILY = 0.05  # 5% daily max drawdown
# Function to get account balance from MetaTrader 5
def get_mt5_balance():
    account_info = mt5.account_info()
    if account_info is None:
        print("Failed to retrieve account info")
        return None
    return account_info.balance

# Function to check drawdown limits
def check_drawdown(initial_balance, start_of_day_balance):
    current_balance = get_mt5_balance()

    if current_balance is None:
        return False

    overall_drawdown = (initial_balance - current_balance) / initial_balance
    daily_drawdown = (start_of_day_balance - current_balance) / start_of_day_balance

    print(f"Current Balance: {current_balance}")
    print(f"Overall Drawdown: {overall_drawdown * 100}%")
    print(f"Daily Drawdown: {daily_drawdown * 100}%")

    if overall_drawdown >= MAX_DRAWDOWN_OVERALL:
        print("Overall maximum drawdown reached. Trading will be suspended.")
        suspend_trading()
        return True

    if daily_drawdown >= MAX_DRAWDOWN_DAILY:
        print("Daily maximum drawdown reached. Trading will be suspended for today.")
        suspend_trading()
        return True

    return False

# Function to suspend trading using Pepperstone API
def suspend_trading():
    # API URL for suspending trading (modify according to Pepperstone API documentation)
    url = f'{PEPPERSTONE_API_URL}/{PEPPERSTONE_ACCOUNT_ID}/suspend'

    # Headers
    headers = {
        'Authorization': f'Bearer {PEPPERSTONE_API_KEY}',
        'Content-Type': 'application/json',
    }

    # Payload to suspend trading
    payload = {
        "status": "suspended",  # Example of suspending the account
        "reason": "Max drawdown reached"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Trading suspended successfully.")
    else:
        print(f"Failed to suspend trading. Error: {response.text}")

# Main trading loop (simplified for the drawdown logic)
def trading_loop():
    initial_balance = INITIAL_BALANCE
    start_of_day_balance = get_mt5_balance()

    while True:
        if check_drawdown(initial_balance, start_of_day_balance):
            break

        # Insert your trading logic here (if trades are to continue during normal conditions)
        time.sleep(60)  # Check every 60 seconds


# Start the trading loop
trading_loop()

# Shutdown MetaTrader 5 when done
mt5.shutdown()
