# --- Configuration ---
# Current USD to INR exchange rate. Update this periodically for accuracy.
USD_TO_INR_EXCHANGE_RATE = 83.50 # Example: As of late 2023 / early 2024

# Gemini 2.5 Pro pricing tiers per 1 Million (1M) tokens in USD
# We convert these to "per 1000 tokens" for easier calculation later.
# 1M tokens = 1000 * 1000 tokens, so divide by 1000 to get cost per 1K tokens.
GEMINI_2_5_PRO_PRICING_USD = {
    "input": {
        "tier1_threshold": 200000, # 200k tokens
        "tier1_price_per_1M_tokens": 1.25, # $1.25 per 1M tokens for <= 200k prompts
        "tier2_price_per_1M_tokens": 2.50, # $2.50 per 1M tokens for > 200k prompts
    },
    "output": {
        "tier1_threshold": 200000, # 200k tokens (for prompt size)
        "tier1_price_per_1M_tokens": 10.00, # $10.00 per 1M tokens for <= 200k prompts
        "tier2_price_per_1M_tokens": 15.00, # $15.00 per 1M tokens for > 200k prompts
    },
    # Context caching and Grounding are not included in this simple token cost function
    # but could be added if you need to track those specific costs.
}

def get_gemini_2_5_pro_cost_string(response):
    """
    Calculates the cost of a Gemini 2.5 Pro query based on its response
    and the provided pricing tiers, returning a formatted string in INR.

    Args:
        response: The response object from genai.GenerativeModel.generate_content().

    Returns:
        A string indicating the cost, input tokens, and output tokens,
        e.g., "This query costs ₹10.78 as there are 785 input token and 5210 output token".
        Returns an error message if token usage metadata is not found.
    """
    input_tokens = 0
    output_tokens = 0

    if response.usage_metadata:
        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
    else:
        return "Error: Token usage metadata not found in the response."

    # --- Calculate Input Cost ---
    input_price_per_1K_tokens_usd = 0.0
    if input_tokens <= GEMINI_2_5_PRO_PRICING_USD["input"]["tier1_threshold"]:
        input_price_per_1K_tokens_usd = GEMINI_2_5_PRO_PRICING_USD["input"]["tier1_price_per_1M_tokens"] / 1000
    else:
        input_price_per_1K_tokens_usd = GEMINI_2_5_PRO_PRICING_USD["input"]["tier2_price_per_1M_tokens"] / 1000

    cost_input_usd = (input_tokens / 1000) * input_price_per_1K_tokens_usd

    # --- Calculate Output Cost ---
    # The output price tier also depends on the *prompt* size
    output_price_per_1K_tokens_usd = 0.0
    if input_tokens <= GEMINI_2_5_PRO_PRICING_USD["output"]["tier1_threshold"]:
        output_price_per_1K_tokens_usd = GEMINI_2_5_PRO_PRICING_USD["output"]["tier1_price_per_1M_tokens"] / 1000
    else:
        output_price_per_1K_tokens_usd = GEMINI_2_5_PRO_PRICING_USD["output"]["tier2_price_per_1M_tokens"] / 1000

    cost_output_usd = (output_tokens / 1000) * output_price_per_1K_tokens_usd

    # Total cost in USD
    total_cost_usd = cost_input_usd + cost_output_usd

    # Convert to INR
    total_cost_inr = total_cost_usd * USD_TO_INR_EXCHANGE_RATE

    # Format the output string
    return (
        f"*This query costs ₹{total_cost_inr:.2f} as there are {input_tokens} input token "
        f"and {output_tokens} output token"
    )