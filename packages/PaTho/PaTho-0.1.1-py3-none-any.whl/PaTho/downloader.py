import argparse
import os
import requests

def download_images(file_path, output_dir, base_url=""):
    """
    Download images from a list of URLs.
    
    Args:
        file_path: Path to file containing URLs.
        output_dir: Path to output directory.
        base_url: Base URL for relative URLs.
        
    Returns:
        None
            
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, "r") as f:
        image_urls = f.readlines()

    # flatten list
    image_urls = [url.strip().split(",") for url in image_urls]
    image_urls = [url for sublist in image_urls for url in sublist]

    # add base url to relative urls
    image_urls = [base_url + url for url in image_urls]

    print(f"Are you sure you want to download {len(image_urls)} images to {output_dir}? (y/n)")
    if input() != "y":
        print("Aborting...")
        return
    
    for url in image_urls:
        print(f"Downloading {url}...")
        r = requests.get(url, allow_redirects=True)
        filename = url.split("/")[-2] + "_" + url.split("/")[-1]
        with open(os.path.join(output_dir, filename), "wb") as f:
            f.write(r.content)

def main():
    parser = argparse.ArgumentParser(description="Download images from a list of URLs.")
    parser.add_argument("-f", "--file", required=True, help="File containing URLs")
    parser.add_argument("-d", "--directory", required=True, help="Output directory for downloaded images")
    parser.add_argument("-b", "--base-url", required=False, help="Base URL for relative URLs", default="")

    args = parser.parse_args()

    download_images(args.file, args.directory, args.base_url)


if __name__ == "__main__":
    main()
