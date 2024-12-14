import os
import re
import pandas as pd
from collections import defaultdict

def read_file_with_fallback_encoding(filepath):
    """Try different encodings to read the file"""
    encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1', 'ascii']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file {filepath}: {str(e)}")
            return None
    
    print(f"Failed to read file with any encoding: {filepath}")
    return None

def parse_filename(filename):
    """Parse configuration from filename"""
    name = filename.replace('_output.txt', '')
    parts = name.split('_')
    
    if len(parts) < 4:
        return None, None, None, None
    
    if 'compress95' in parts[0]:
        app = 'compress95'
    else:
        app = parts[0]
    
    for part in parts:
        if part.startswith('b'):
            try:
                block_size = int(part[1:])
            except ValueError:
                continue
        elif part.startswith('a'):
            try:
                associativity = int(part[1:])
            except ValueError:
                continue
        elif part in ['fifo', 'lru', 'random']:
            replacement = part
    
    return app, block_size, associativity, replacement

def parse_simulation_file(filepath):
    """Extract simulation metrics from file"""
    metrics = {}
    
    content = read_file_with_fallback_encoding(filepath)
    if content is None:
        return None
        
    patterns = {
        'sim_num_insn': r'sim_num_insn\s+(\d+)',
        'sim_num_loads': r'sim_num_loads\s+(\d+)',
        'sim_num_branches': r'sim_num_branches\s+(\d+)',
        'sim_cycle': r'sim_cycle\s+(\d+)',
        'sim_IPC': r'sim_IPC\s+(\d+\.\d+)',
        'sim_CPI': r'sim_CPI\s+(\d+\.\d+)'
    }
    
    for metric, pattern in patterns.items():
        match = re.search(pattern, content)
        if match:
            value = match.group(1)
            metrics[metric] = float(value) if '.' in value else int(value)
    
    return metrics

def process_simulation_results(directory):
    """Process simulation output files in specified directory"""
    results = []
    
    files = [f for f in os.listdir(directory) if '_output.txt' in f]
    print(f"Found {len(files)} output files")
    
    for filename in files:
        filepath = os.path.join(directory, filename)
        app, block_size, associativity, replacement = parse_filename(filename)
        
        if None in (app, block_size, associativity, replacement):
            print(f"Skipping file with invalid format: {filename}")
            continue
        
        metrics = parse_simulation_file(filepath)
        if metrics is None:
            continue
        
        result = {
            'Application': app,
            'Block_Size': block_size,
            'Associativity': associativity,
            'Replacement': replacement,
            **metrics
        }
        
        results.append(result)
        print(f"Processed: {app}_{replacement} ({block_size}-{associativity})")
    
    return results

def generate_csv_tables(results):
    """Generate CSV content for each application-replacement combination"""
    if not results:
        return []
    
    df = pd.DataFrame(results)
    df['config'] = df['Block_Size'].astype(str) + '-' + df['Associativity'].astype(str)
    
    metrics = ['sim_num_insn', 'sim_num_loads', 'sim_num_branches', 
              'sim_cycle', 'sim_IPC', 'sim_CPI']
    
    csv_tables = []
    
    for app in sorted(df['Application'].unique()):
        app_df = df[df['Application'] == app]
        for replacement in sorted(app_df['Replacement'].unique()):
            configs = sorted(app_df['config'].unique(), 
                           key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))
            
            header = f"{app.upper()}_{replacement.upper()}"
            header_row = [header] + configs
            
            filtered_df = app_df[app_df['Replacement'] == replacement]
            data_rows = []
            
            for metric in metrics:
                row = [metric]
                for config in configs:
                    value = filtered_df[filtered_df['config'] == config][metric].iloc[0]
                    row.append(str(value))
                data_rows.append(row)
            
            table = [header_row] + data_rows
            csv_tables.append(table)
    
    return csv_tables

def save_csv_tables(tables, output_dir):
    """Save CSV tables to separate files"""
    if not tables:
        print("No tables to save")
        return
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"\nSaving tables to {output_dir}")
        
        for table in tables:
            filename = f"{table[0][0]}.csv"
            filepath = os.path.join(output_dir, filename)
            
            df = pd.DataFrame(table[1:], columns=table[0])
            df.to_csv(filepath, index=False)
            print(f"Saved {filename}")
            
            print(f"\nPreview of {filename}:")
            print(df.to_string())
            print("\n" + "="*80 + "\n")
            
    except Exception as e:
        print(f"Error saving tables: {str(e)}")

def main():
    directory = r"C:\Users\LSJ\Downloads\CA_project\test_5"
    output_dir = os.path.join(directory, "results")
    
    print("Processing simulation results...")
    results = process_simulation_results(directory)
    
    if results:
        print(f"\nFound {len(results)} valid simulation results")
        tables = generate_csv_tables(results)
        save_csv_tables(tables, output_dir)
    else:
        print("No valid simulation results found")

if __name__ == "__main__":
    main()
