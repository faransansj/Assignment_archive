import itertools

# Parameters
block_sizes = [32, 64, 128]
associativities = [2, 4, 8]
applications = ['anagram', 'compress95', 'go']
policy = 'r'  # Random replacement policy

def generate_config(block_size, assoc):
    return f'''-fetch:ifqsize                    4
-fetch:mplat                      3
-fetch:speed                      1
-bpred                        bimod
-bpred:bimod           2048
-bpred:2lev            1 1024 8 0
-bpred:comb            1024
-bpred:ras                        8
-bpred:btb             512 4
-decode:width                     4
-issue:width                      4
-issue:inorder                false
-issue:wrongpath               true
-commit:width                     4
-ruu:size                        16
-lsq:size                         8
-cache:dl1             dl1:128:{block_size}:{assoc}:{policy}
-cache:dl1lat                     1
-cache:dl2             ul2:1024:{block_size}:{assoc}:{policy}
-cache:dl2lat                     6
-cache:il1             il1:512:32:1:l
-cache:il1lat                     1
-cache:il2                      dl2
-cache:il2lat                     6
-cache:flush                  false
-cache:icompress              false
-mem:lat               18 2
-mem:width                        8
-tlb:itlb              itlb:16:4096:4:l
-tlb:dtlb              dtlb:32:4096:4:l
-tlb:lat                         30
-res:ialu                         4
-res:imult                        1
-res:memport                      2
-res:fpalu                        4
-res:fpmult                       1
-bugcompat                    false'''

# Generate all combinations for each application
for app in applications:
    for block_size, assoc in itertools.product(block_sizes, associativities):
        filename = f"{app}_b{block_size}_a{assoc}_random.cfg"
        config = generate_config(block_size, assoc)
        
        with open(filename, 'w') as f:
            f.write(config)
        print(f"Generated {filename}")

print("\nConfiguration files have been created.")
