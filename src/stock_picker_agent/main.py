#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from stock_picker_agent.crew import StockPickerAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "sector": "technology",
        "current_date": datetime.now().strftime("%m-%d-%Y"),
    }
    result = None
    try:
        result = StockPickerAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    finally:
        print("\n\n=== FINAL DECISION ===\n\n")
        if result is not None:
            print(result.raw)
        else:
            print("No result returned from the crew.")

if __name__ == "__main__":
    run()

