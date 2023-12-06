from datetime import datetime
import urllib.request
import basc_py4chan
import argparse
import shutil
import timeit
import tqdm
import json
import csv
import os

def scrape4chan_board(board_name, num_threads, debug=False):
    def get_board_info(board_name):
        board = basc_py4chan.Board(board_name)
        board.refresh_cache(if_want_update=True)
        all_thread_ids = board.get_all_thread_ids()
        board_metadata = (f'Board Title: {board.title}\n'
                          f'Number of Threads Currently: {len(all_thread_ids)}\n'
                          f'Number of Threads to Scrape: {num_threads}\n')
        return board, all_thread_ids, board_metadata

    def write_thread_data(thread, filepath):
        if thread.expand() is not None:
            thread.expand()
        if thread.update(force=True) is not None:
            num_new_posts = thread.update(force=True)
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write((f"Thread ID: {thread_id}\n"
                     f"Sticky?: {thread.sticky if thread.sticky is not None else 'None'}\n"
                     f"Closed?: {thread.closed}\n"
                     f"Archived: {thread.archived}\n"
                     f"Number of Posts on Thread: {len(thread.posts)}\n"
                     f"JSON URL: {basc_py4chan.Url('pol').thread_api_url(thread_id)}\n"
                     f"Number of Replies on Thread: {len(thread.replies)}\n"
                     f"Number of New Posts: {num_new_posts if num_new_posts > 0 else 0}\n"))

    def download_file(post, url, path):
        try:
            urllib.request.urlretrieve(post.file_url, path)
        except Exception as e:
            if debug:
                print(f"Error downloading {post.filename}.\n")

    def write_file_data(post, filepath):
        with open(filepath, 'a', encoding='utf-8') as f:
            if post.has_file:
                f.write((f'Filename: {post.filename}\n'
                         f'File Size: {post.file_size} bytes\n'
                         f'MD5 Hash: {post.file_md5_hex}\n'
                         f'File URL: {post.file_url}\n'
                         f'Thumbnail URL: {post.thumbnail_url}\n\n'))
            f.close()

    def make_safe_filename(string):
        safe_char = lambda c: c if c.isalnum() else "_"
        return "".join(safe_char(c) for c in string).rstrip("_")

    def download_json_thread(local_filename, url):
        with open(local_filename, 'w', encoding='utf-8') as json_file:
            try:
                thread_json_data = json.loads(urllib.request.urlopen(url).read())
                json_file.write(json.dumps(thread_json_data, sort_keys=False, indent=4, separators=(',', ': ')))
                json_file.close()
            except Exception as e:
                if debug:
                    print(f'Error downloading {local_filename}.\n')

    def mkdir(path, mode):
        try:
            if not (os.path.exists(path)):
                os.mkdir(path, mode)
            else:
                if debug:
                    print(f'"{path}" already created.')
        except Exception as e:
            if debug:
                print(f'Failed to create directory {path}.\n')

    def archive_data(board_name, board_name_dir):
        try:
            if debug:
                print('\nCompressing Data...')
            shutil.make_archive(f'{board.name} - {datetime.now().strftime("%b-%d-%Y  %H-%M-%S")}', 'zip',
                                f'{board_name_dir}')
            shutil.rmtree(f'{board_name_dir}')
            if debug:
                print('Data compressed!')
        except Exception as e:
            if debug:
                print('Error compressing data.\n')

    def write_comments_csv(post, filepath):
        comment = post.text_comment.encode('utf-8').decode('utf-8')
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if os.stat(filepath).st_size == 0:
                writer.writerow(['post_id', 'date_time', 'subject', 'comment/reply', 'name', 'is_op?', 'url'])
            writer.writerow([post.post_id, post.datetime.strftime("%b-%d-%Y, %H:%M:%S"),
                             post.subject if post.subject is not None else 'No Subject',
                             '(REPLY) ' + comment if ">>" in comment and not (post.is_op) else comment,
                             post.name.encode('utf-8').decode('utf-8') if post.name is not None else 'No Name',
                             post.is_op, post.semantic_url])
        f.close()

    try:
        parser = argparse.ArgumentParser()  # Define the parser here
        board, all_thread_ids, board_metadata = get_board_info(board_name)
        print(f'\nBeginning 4Chan Catalog Scrape on /{board.name}/', '\n---------------------------------------')
        print('Current Date and Time:', datetime.now().strftime("%b-%d-%Y, %H:%M:%S"))

        # Defining file structure paths
        board_name_dir = f'{board.name}/'

        # Print Board Information
        print(board_metadata)
        if num_threads and (num_threads <= 0 or num_threads > len(all_thread_ids)):
            parser.error(f"Number of threads not in range: {[1, len(all_thread_ids)]}\n")

        print('Processing...\n')

        if debug:
            print('Subject Names Scraped:\n-------------------------')

        # Start runtime execution timer
        start = timeit.default_timer()

        # Create directory for board name
        mkdir(board_name_dir, 0o0666)

        # Check if a given thread is not 404'd
        if board.thread_exists:
            # Loop for each thread in the thread ID list
            for thread_id in tqdm.tqdm(all_thread_ids[0: num_threads], desc='Scraping Progress'):
                thread = board.get_thread(thread_id)

                # Defining additional file structure paths
                if thread.posts is not None:
                    subject = thread.posts[0].subject
                    if debug:
                        print("\n\n" + subject if subject is not None else '\n\nNo Subject')
                    if subject is not None:
                        thread_id_dir = f'{board.name}/{thread_id} - {make_safe_filename(subject)}'
                    else:
                        thread_id_dir = f'{board.name}/{thread_id} - No Subject'

                    images_dir = f'{thread_id_dir}/{thread_id} files/'

                # Create directory structure for thread
                mkdir(thread_id_dir, 0o0666)
                mkdir(images_dir, 0o0666)

                # Download JSON for thread via catalog URL
                json_url = basc_py4chan.Url(board_name).thread_api_url(thread_id)
                download_json_thread(f'{thread_id_dir}/{thread_id}.json', json_url)

                # Write thread information to .txt
                write_thread_data(thread, f'{thread_id_dir}/{thread_id} - thread metadata.txt')

                # Post Information
                if thread.posts is not None:
                    for post in thread.posts:

                        # Write comments and replies to CSV file
                        write_comments_csv(post, f'{thread_id_dir}/{thread_id} - comments & replies.csv')

                        # Write file metadata to .txt
                        if post.has_file:
                            write_file_data(post, f'{thread_id_dir}/{thread_id} - file metadata.txt')
                            download_file(post, post.file_url, f'{images_dir}' + post.filename)

        # Zip up and remove board name folder
        archive_data(board.name, board_name_dir)
    except (Exception, KeyboardInterrupt):
        print(f'An error occurred. Deleting /{board.name}/ folder in {os.getcwd()}.')
        shutil.rmtree(f'{board_name_dir}')
        exit(f'{board.name} successfully removed! Please rerun again!')

    # Finish scraping / end runtime execution timer
    end = timeit.default_timer()
    print('\nScraping Complete!')
    print("Total Runtime Execution:", round(end - start, 3), "seconds")
