Delete reinsert logic

# Debug and reinsert
# Use try-except blocks to handle exceptions.
# Transactions (commit and rollback) should be used.
def parseGarinGPS(self, sensor_id, bag_file_id, bag_file, topic, output_file_name):
    file = open(output_file_name, "w")
    number_of_messages = bag_file.get_message_count(topic_filters=topic)
    count = 0
    try:
        for topic, msg, t in bag_file.read_messages(topics=[topic]):
            # Process message and write to file...
            count += 1
        file.close()

        # Try to insert data
        self.db.bulk_insert(table='garmin_gps', fields=[...], file_name=output_file_name)
    except Exception as e:
        print(f"Error while parsing or inserting: {e}")
        self.db.conn.rollback()
        # Delete and reinsert data
        if self.replace_all or input('Data exists. Overwrite? [y/n/a]') == 'y':
            self.db.delete(table='garmin_gps', where=[f'bag_files_id={bag_file_id}'])
            self.db.bulk_insert(table='garmin_gps', fields=[...], file_name=output_file_name)
        else:
            return  # Optionally handle the case where reinsertion is not done
    finally:
        if file: file.close()

    print("Insert Garmin_gps to database successfully!")
