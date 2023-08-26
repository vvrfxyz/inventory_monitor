import datetime
import logging
import time
import yaml
from box import Box
from monitor import Monitor, send_notification, is_within_time_range
from onepush import get_notifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    # Initialize notifier
    bark = get_notifier('bark')

    # Load configuration
    logging.info("Loading configuration from config.yml")
    with open("config.yml", "r", encoding='utf-8') as file:
        config = yaml.safe_load(file)
    logging.info("Configuration loaded successfully")

    sleep_interval = config.get("sleep_interval", 10)  # 提供默认值
    logging.info(f"Using sleep interval of {sleep_interval} seconds")

    bark_key = config["bark"]["key"]
    global_headers = config["global_headers"]
    websites_config = config["websites"]

    # Set time range for monitoring
    time_settings = config.get('time_settings', {})
    start_time = time_settings.get('start', '00:00')
    end_time = time_settings.get('end', '23:59')
    logging.info(f"Monitoring time range set from {start_time} to {end_time}")

    # Convert website configurations to Box objects for easier access
    website_boxes = [Box(web) for web in websites_config]

    monitor_instance = Monitor()
    monitor_instance.session.headers.update(global_headers)

    logging.info("Beginning monitoring loop")
    while True:
        if is_within_time_range(start_time, end_time):
            current_time = datetime.datetime.now()
            logging.info(f"Current time: {current_time}")

            for web_config in website_boxes:
                if not web_config.get('active', True):
                    logging.info(f"Skipping inactive website: {web_config.get('name')}")
                    continue

                stock = monitor_instance.monitor_stock(web_config)
                if stock and stock > 0:
                    logging.info(f"Stock detected for {web_config['name']}. Sending notification.")
                    send_notification(bark, bark_key, web_config['title'], web_config['message'])
                else:
                    logging.info(f"No stock detected for {web_config['name']}.")

            logging.info(f"Sleeping for {sleep_interval} seconds before next iteration")
            time.sleep(sleep_interval)

if __name__ == '__main__':
    logging.info("Starting the monitoring script")
    main()
    logging.info("Monitoring script terminated")
