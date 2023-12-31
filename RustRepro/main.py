import json
import os
import shutil
import subprocess
from multiprocessing import Pool
from typing import List
from enum import Enum

# import req
import requests


class ReproStatus(Enum):
    # Successful reproduction
    SUCCESS = 1
    # Differences found
    NON_REPRODUCTION = 2
    # Differences found but the package uses build script or proc macro
    NON_REPRODUCTION_WITH_THIRD_PARTY_BUILD_CODE = 3
    # Other build failures
    BUILD_FAILED = 4


def run_reprotest(name: str, repository: str, reprotest_args: List[str]) -> [ReproStatus, List[str]]:
    
    # Check if the repository is already cloned
    if not os.path.exists(name):
        with subprocess.Popen(
                ["git", "clone", "--depth", "1", repository, name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
        ) as git:
            for line in git.stdout:
                print(line, end="")

        # if git.wait() != 0:
        #     return[ ReproStatus.BUILD_FAILED, None, reprotest_args[0].split("+")[1]]

    output = []
    with subprocess.Popen(
            ["sudo", "reprotest", "-s", name, *reprotest_args],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
    ) as reprotest:
        if reprotest_args[0].split("=")[0] == "--config-file":
            reprotest_args[0] = "+all"
        for line in reprotest.stdout:
            print(line, end="")
            output.append(line)

        if reprotest.wait() == 0:
            status = [ReproStatus.SUCCESS, None, reprotest_args[0].split("+")[1]]
        elif any(line.lstrip().startswith("---") for line in output) and any(
                line.lstrip().startswith("+++") for line in output
        ):
            # we don't really have a better way to detect the failure was from diffoscope
            if any(line.startswith("MEAN-RUSTC-WARN") for line in output):
                status = [ReproStatus.NON_REPRODUCTION_WITH_THIRD_PARTY_BUILD_CODE, output, reprotest_args[0].split("+")[1] ]
            else:
                status = [ReproStatus.NON_REPRODUCTION, output, reprotest_args[0].split("+")[1]]
        else:
            status = [ReproStatus.BUILD_FAILED, output, reprotest_args[0].split("+")[1]]

    # shutil.rmtree(name)
    return status


def pull_repos():
    # https://libraries.io/search?languages=Go&order=desc&platforms=Go&sort=stars
    page = 1
    # https://libraries.io/search?keywords=rust&languages=Rust&order=desc&platforms=Cargo

    resources = []

    while len(resources) < 400:
        url = "https://libraries.io/api/search?api_key=141f39abc3f98e29647df1b93f02afaf&languages=Rust&order=desc&page=" \
              "{}&platforms".format(page) + "=Cargo"

        response = requests.get(url)
        data = response.json()
        for item in data:
            try:
                if str(item['repository_url']).startswith("https://github.com"):
                    d = {
                        "project": item['name'],
                        "url": item['repository_url'],
                        "stars": item['stars'],
                    }
                    resources.append(d)
            except:
                print("Error")

        page += 1
        print(url)
        print(len(resources))

    with open('data/cargo_400.json', 'w') as outfile:
        final = {"data": resources}
        json.dump(final, outfile)
def convert_csv():
    with open('data/cargo400Results.json', 'r') as f:
        records = json.load(f)['results']

        # If len(records) > 400: records = records[:400]

        # if len(records) > 400:
        #     # Radomly select 400
        #     records = random.sample(records, 400)

        s = open('data/cargo400Results.csv', 'w')
        s.write("project, status, reproducibleVariants, nonReproducibleVariants, stars\n")
        for i in range(len(records)):
            s.write("{}, {}, {}, {}, {}\n".format(
                records[i]['project'],
                records[i]['status'],
                str(records[i]['variationsReproducible']).replace(',', ';'),
                str(records[i]['variationsNonReproducible']).replace(',', ';'),
                records[i]['stars']))
        s.close()

        # Save the randomly sampled records
        with open('data/go_Random400Results.json', 'w') as f:
            json.dump({"results": records}, f)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # convert_csv()
    # pull_repos()
    # fixStars()
    # print_hi('PyCharm')
    # raise Exception("wahala")
    with open('data/cargo_400.json', 'r') as f:
        records = json.load(f)['data']
        f.close()

    for record in records:
        print(record)
        name = record['project']
        url = record['url']
        stars = record['stars']
        print(name, url, stars)

        possible_variations = ["environment", "fileordering", "home", "kernel", "locales", "exec_path", "time", "timezone", "umask"]
        # test all
        if not os.path.exists('/home/osolarin/ReproducibleTests/RustRepro/data/diffoscopeLogs{}'.format(name)):
            os.mkdir('/home/osolarin/ReproducibleTests/RustRepro/data/diffoscopeLogs{}'.format(name))

        if not os.path.exists('/home/osolarin/ReproducibleTests/RustRepro/data/diffoscopeLogs{}/{}'.format(name,
                                                                                                           url.replace(
                                                                                                               "/",
                                                                                                               "_"))):
            os.mkdir('/home/osolarin/ReproducibleTests/RustRepro/data/diffoscopeLogs{}/{}'.format(name,
                                                                                                  url.replace("/",
                                                                                                              "_")))

        all = run_reprotest(name, url, ["--config-file=/home/osolarin/ReproducibleTests/RustRepro/.reprotestrc", "sudo cargo package", "target/package/*.crate*"])

        if all[0] == ReproStatus.SUCCESS:
            print("Success")
            # Its reproducible
            record = json.loads(
                open('/home/osolarin/ReproducibleTests/RustRepro/data/{}.json'.format("cargo400Results"), 'r').read())[
                "results"]
            record.append({
                "project": name,
                "stars": stars,
                "status": "Fully Reproducible",
                "variationsNonReproducible": [],
                "variationsReproducible": ["all"]
            })

            # write to file
            with open('/home/osolarin/ReproducibleTests/RustRepro/data/{}.json'.format("cargo400Results"), 'w') as f:
                json.dump({"results": record}, f)
                f.close()



        else:

            # Try all other variations
            variations_reproducible = []
            variations_not_reproducible = []
            variation_errors = []

            # Use multiprocessing to run reprotest commands in parallel
            pool = Pool()
            results = pool.starmap(run_reprotest,
                                   [(name, url, ["--variation=+{}".format(variation), "sudo cargo build --release", "target/*"]) for variation in
                                    possible_variations])
            pool.close()
            pool.join()
            shutil.rmtree(name)


            for result in results:
                if result[0] == ReproStatus.SUCCESS:
                    variations_reproducible.append(result[2])
                elif result[0] == ReproStatus.NON_REPRODUCTION:
                    variations_not_reproducible.append(result[2])
                else:
                    variation_errors.append(result[2])

            # Record the results
            record = json.loads(
                open('/home/osolarin/ReproducibleTests/RustRepro/data/{}.json'.format("cargo400Results"),
                     'r').read())[
                "results"]
            record.append({
                "project": name,
                "stars": stars,
                "status": "Partially Reproducible" if len(variations_reproducible) > 0 else "Not Reproducible",
                "variationsNonReproducible": variations_not_reproducible,
                "variationsReproducible": variations_reproducible,
                "variationErrors": variation_errors
            })

            print(record)

            with open('/home/osolarin/ReproducibleTests/RustRepro/data/{}.json'.format("cargo400Results"), 'w') as f:
                json.dump({"results": record}, f)



