import json
import time
import websocket

# Configuration
API_TOKEN = "YOUR_DERIV_API_TOKEN_HERE"  # Replace with your API token
APP_ID = "1089"                          # Replace with your App ID
SYMBOL = "R_100"                         # e.g., Volatility 100 Index or Step Index
AMOUNT = 10                              # Stake amount

def on_open(ws):
    print("Connected to Deriv WebSocket API")
    # Authenticate
    auth_req = {"authorize": API_TOKEN}
    ws.send(json.dumps(auth_req))

def on_message(ws, message):
    data = json.loads(message)
    msg_type = data.get("msg_type")

    # Handle Authorization Success
    if msg_type == "authorize":
        print("Authorization successful! Subscribing to market ticks...")
        # Subscribe to live price ticks
        ticks_req = {"ticks": SYMBOL}
        ws.send(json.dumps(ticks_req))

    # Process Price Ticks & Strategy Logic
    elif msg_type == "tick":
        tick_price = data["tick"]["quote"]
        print(f"Live Price [{SYMBOL}]: {tick_price}")

        # Place your strategy conditions here (e.g., RSI/Stochastic indicators)
        # Example Buy Execution Trigger:
        # execute_trade(ws, "CALL", AMOUNT)

def execute_trade(ws, contract_type, amount):
    """Executes a trade order on Deriv"""
    proposal_req = {
        "buy": 1,
        "price": amount,
        "parameters": {
            "amount": amount,
            "basis": "stake",
            "contract_type": contract_type,  # "CALL" for Buy, "PUT" for Sell
            "currency": "USD",
            "duration": 5,
            "duration_unit": "t",            # Duration in ticks/minutes
            "symbol": SYMBOL
        }
    }
    ws.send(json.dumps(proposal_req))
    print(f"Order sent: {contract_type} with stake {amount}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed. Reconnecting in 5 seconds...")
    time.sleep(5)
    run_bot()

def run_bot():
    ws_url = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    run_bot()
