import hashlib
import time
import itertools
import tqdm

hash = "67ae1a64661ac8b4494666f58c4822408dd0a3e4"
Dict = {'q': 'Q', 'w': 'W', 'n': 'N', '5': '%', '(': '8', '0': '=', 'i': 'I', '+': '*'}

def get_sha1(str):
    return hashlib.sha1(str.encode()).hexdigest()

s = "".join(Dict.keys())
print(f"init string: {s}")

start_time = time.time()
for cnt in tqdm.trange(1<<len(s)):
    tmp = s
    for i in range(len(s)):
        if (1<<i) & cnt > 0:
            tmp = tmp.replace(tmp[i],Dict[tmp[i]])
    for x in itertools.permutations(tmp,len(tmp)): 
        if get_sha1("".join(x)) == hash:
            print("\nans: ","".join(x))
            end_time = time.time()
            runtime = end_time - start_time
            print(runtime)
            exit(0)

