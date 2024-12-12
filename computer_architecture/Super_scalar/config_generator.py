import itertools

# Parameters
block_sizes = [32, 64, 128]
associativities = [2, 4, 8]
applications = {
    'anagram': 'T1_anagram.cfg',
    'compress95': 'T1_compress95.cfg',
    'go': 'T1_go.cfg',
    'gcc': 'T1_gcc.cfg'
}
policies = {
    'FIFO': 'f',
    'LRU': 'l',
    'RANDOM': 'r'
}

def modify_cache_config(template_file, new_file, block_size, assoc, policy_char):
    with open(template_file, 'r') as f:
        content = f.readlines()
    
    for i, line in enumerate(content):
        if '-cache:dl1             dl1:' in line:
            content[i] = f'-cache:dl1             dl1:128:{block_size}:{assoc}:{policy_char}\n'
        elif '-cache:dl2             ul2:' in line:
            content[i] = f'-cache:dl2             ul2:1024:{block_size}:{assoc}:{policy_char}\n'
    
    with open(new_file, 'w', newline='') as f:
        f.writelines(content)

# Calculate total expected configurations
total_configs = len(applications) * len(block_sizes) * len(associativities) * len(policies)
print(f"Starting generation of {total_configs} configuration files...\n")

# Generate configurations for each application
counter = 0
for app, template in applications.items():
    for block_size, assoc, (policy_name, policy_char) in itertools.product(block_sizes, associativities, policies.items()):
        new_filename = f"{app}_b{block_size}_a{assoc}_{policy_name.lower()}.cfg"
        try:
            modify_cache_config(template, new_filename, block_size, assoc, policy_char)
            
            # Verify the file was created correctly
            with open(new_filename, 'r') as f:
                if not f.read():
                    print(f"Warning: {new_filename} is empty!")
                else:
                    counter += 1
                    print(f"Generated {new_filename} ({counter}/{total_configs})")
        except Exception as e:
            print(f"Error generating {new_filename}: {str(e)}")

print(f"\nConfiguration files generation complete.")
print(f"Total files generated: {counter}")
print(f"Files per application: {len(block_sizes) * len(associativities) * len(policies)}")
print(f"Applications processed: {len(applications)}")
print(f"\nBreakdown:")
print(f"- Applications: {len(applications)} (anagram, compress95, go, gcc)")
print(f"- Block sizes: {len(block_sizes)} ({', '.join(map(str, block_sizes))})")
print(f"- Associativities: {len(associativities)} ({', '.join(map(str, associativities))})")
print(f"- Policies: {len(policies)} ({', '.join(policies.keys())})")
print(f"Total combinations: {len(applications)} × {len(block_sizes)} × {len(associativities)} × {len(policies)} = {total_configs}")
