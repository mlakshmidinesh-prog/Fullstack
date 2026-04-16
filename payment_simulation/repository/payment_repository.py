from db_config import get_db_connection

def process_payment(user_id, merchant_id, amount):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check user balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        user_balance = cursor.fetchone()
        if not user_balance:
            return "User not found"
        if user_balance[0] < amount:
            return "Insufficient balance"

        # Deduct from user
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))

        # Add to merchant
        cursor.execute("UPDATE merchants SET balance = balance + %s WHERE merchant_id = %s", (amount, merchant_id))

        # Commit transaction
        conn.commit()
        return "Payment successful"

    except Exception as e:
        conn.rollback()
        return f"Payment failed: {str(e)}"

    finally:
        cursor.close()
        conn.close()
