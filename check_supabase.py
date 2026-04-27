import os
from supabase import create_client
from dotenv import load_dotenv

def validate():
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env or environment.")
        return

    print(f"Connecting to: {url}...")
    try:
        supabase = create_client(url, key)
        
        # Test 1: Check if 'cvs' table exists
        print("Checking tables...")
        try:
            supabase.table('cvs').select('id').limit(1).execute()
            print("✅ 'cvs' table found.")
        except Exception as e:
            print(f"❌ Error: 'cvs' table not found or accessible. Did you run the SQL schema?")
            print(f"   Detail: {e}")
            return

        # Test 2: Check related tables
        for table in ['experience', 'education', 'skills']:
            try:
                supabase.table(table).select('id').limit(1).execute()
                print(f"✅ '{table}' table found.")
            except:
                print(f"❌ Error: '{table}' table not found.")
                return

        print("\n🎉 Your Supabase database is properly configured and ready!")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    validate()
