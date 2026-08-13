"""
Test script to verify the updated GetSymbolRussell1000.py works correctly
with the new Wikipedia URL.
"""

import sys
import os
import pandas as pd
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import the Model, View, Control classes
from mvc.controllers.GetSymbolRussell1000 import Model, View, Control


def test_fetch_russell_1000():
    """Test fetching Russell 1000 data from the new Wikipedia URL"""
    logger.info("=" * 60)
    logger.info("Testing Russell 1000 Data Fetch")
    logger.info("=" * 60)

    # Create a temporary CSV file for testing
    test_csv = "test_russell1000_temp.csv"

    try:
        # Initialize the model with the new URL
        model = Model(
            "https://en.wikipedia.org/wiki/List_of_Russell_1000_companies",
            test_csv,
            "Company",
        )

        # Create controller
        control = Control(model, View())

        # Step 1: Test fetching HTML
        logger.info("\n[STEP 1] Fetching HTML data from Wikipedia...")
        try:
            df_raw = model.readHtml()
            logger.info(f"✓ Successfully fetched data")
            logger.info(f"  - Rows retrieved: {len(df_raw)}")
            logger.info(f"  - Columns: {list(df_raw.columns)}")

            if len(df_raw) == 0:
                logger.error("✗ FAILED: No data retrieved from Wikipedia")
                return False

            if len(df_raw) < 900:
                logger.warning(
                    f"⚠ WARNING: Expected ~1000 rows, got {len(df_raw)}"
                )
            else:
                logger.info(
                    f"✓ Data volume looks good (~{len(df_raw)} companies)"
                )

        except Exception as e:
            logger.error(f"✗ FAILED to fetch HTML: {e}")
            return False

        # Step 2: Test data cleaning
        logger.info("\n[STEP 2] Cleaning and transforming data...")
        try:
            control.cleanData()
            logger.info(f"✓ Data cleaning successful")
            logger.info(f"  - Cleaned columns: {list(model.df.columns)}")

            # Verify expected columns exist
            if (
                "symbol" not in model.df.columns
                or "name" not in model.df.columns
            ):
                logger.error(
                    f"✗ FAILED: Expected columns 'symbol' and 'name' not found"
                )
                logger.error(f"  Available columns: {list(model.df.columns)}")
                return False

            logger.info(f"✓ Required columns 'symbol' and 'name' found")

        except Exception as e:
            logger.error(f"✗ FAILED to clean data: {e}")
            logger.error(
                f"  Available columns in raw data: {list(df_raw.columns)}"
            )
            return False

        # Step 3: Test data saving
        logger.info("\n[STEP 3] Saving data to CSV...")
        try:
            control.saveData()

            if not os.path.exists(test_csv):
                logger.error(
                    f"✗ FAILED: CSV file '{test_csv}' was not created"
                )
                return False

            logger.info(f"✓ CSV file created successfully: {test_csv}")

            # Verify the saved data
            saved_df = pd.read_csv(test_csv)
            logger.info(f"  - Rows in CSV: {len(saved_df)}")
            logger.info(f"  - Columns in CSV: {list(saved_df.columns)}")

        except Exception as e:
            logger.error(f"✗ FAILED to save data: {e}")
            return False

        # Step 4: Verify data integrity
        logger.info("\n[STEP 4] Verifying data integrity...")
        try:
            saved_df = pd.read_csv(test_csv)

            # Check for null values
            null_symbols = saved_df["symbol"].isnull().sum()
            null_names = saved_df["name"].isnull().sum()

            if null_symbols > 0 or null_names > 0:
                logger.warning(
                    f"⚠ WARNING: Found null values - symbols: {null_symbols}, names: {null_names}"
                )
            else:
                logger.info(
                    f"✓ No null values found in symbol or name columns"
                )

            # Check for duplicates
            dup_symbols = saved_df["symbol"].duplicated().sum()
            if dup_symbols > 0:
                logger.warning(
                    f"⚠ WARNING: Found {dup_symbols} duplicate symbols"
                )
            else:
                logger.info(f"✓ No duplicate symbols found")

            # Show sample data
            logger.info(f"\n[SAMPLE DATA] First 5 rows:")
            logger.info(f"\n{saved_df.head().to_string()}")

            logger.info(f"\n[SAMPLE DATA] Last 5 rows:")
            logger.info(f"\n{saved_df.tail().to_string()}")

        except Exception as e:
            logger.error(f"✗ FAILED to verify data: {e}")
            return False

        logger.info("\n" + "=" * 60)
        logger.info("✓ ALL TESTS PASSED")
        logger.info("=" * 60)
        return True

    finally:
        # Cleanup: Remove temporary test file
        if os.path.exists(test_csv):
            try:
                os.remove(test_csv)
                logger.info(
                    f"\n[CLEANUP] Removed temporary test file: {test_csv}"
                )
            except Exception as e:
                logger.warning(f"Could not remove temporary file: {e}")


def test_compare_with_existing():
    """Compare new implementation with the existing asset list (if it exists)"""
    logger.info("\n" + "=" * 60)
    logger.info("Comparing with existing Russell 1000 asset list")
    logger.info("=" * 60)

    existing_csv = "asset_list/Russell1000.csv"

    if not os.path.exists(existing_csv):
        logger.info(f"ℹ No existing asset list found at {existing_csv}")
        logger.info("  Run the main script to generate the new list")
        return True

    try:
        existing_df = pd.read_csv(existing_csv)
        logger.info(f"\nExisting asset list statistics:")
        logger.info(f"  - Total symbols: {len(existing_df)}")
        logger.info(f"  - Columns: {list(existing_df.columns)}")

        # Show sample
        logger.info(f"\nFirst 3 symbols:")
        logger.info(f"\n{existing_df.head(3).to_string()}")

        return True

    except Exception as e:
        logger.error(f"Error reading existing asset list: {e}")
        return False


if __name__ == "__main__":
    # Run tests
    success = test_fetch_russell_1000()
    test_compare_with_existing()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
