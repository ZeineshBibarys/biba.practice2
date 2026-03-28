import json
import re

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    data = {
        "date": None,
        "time": None,
        "items": [],
        "total": 0.0,
        "payment_method": None
    }

    for i in range(len(lines)):
        line = lines[i]

        if "Время:" in line:
            parts = line.split(" ")
            data["date"] = parts[1]
            data["time"] = parts[2]

        elif line == "ИТОГО:":
            total_str = lines[i+1]
            clean_total = total_str.replace(' ', '').replace(',', '.')
            data["total"] = float(clean_total)

        elif "Банковская карта" in line:
            data["payment_method"] = "Банковская карта"
        elif "Наличные" in line:
            data["payment_method"] = "Наличные"

        
        elif re.match(r'^\d+\.$', line):
            
            product_name = lines[i+1]
            
            qty_price_line = lines[i+2]

            if ' x ' in qty_price_line:
                qty_str, price_str = qty_price_line.split(' x ')
                
                clean_price = price_str.replace(' ', '').replace(',', '.')
                
                data["items"].append({
                    "product": product_name,
                    "price": float(clean_price)
                })

    return data

if __name__ == "__main__":
    receipt_data = parse_receipt('raw.txt')
    print(json.dumps(receipt_data, indent=4, ensure_ascii=False))