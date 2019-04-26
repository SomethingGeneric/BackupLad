import os,sys,shutil,time,datetime

def verify(path):
    if os.path.exists(path):
        return 1
    else:
        return 0

class anbackup:
    def __init__(self):
        if not verify("backup.config"):
            self.dat_path = input("Folder to save: ")
            self.backup_folder = input("Folder to fill with backups: ")
            self.handle_loop = int(input("Should this program handle scheduling? (1: yes, or any other # for no): "))
            if self.handle_loop == 1:
                self.delay = int(input("Seconds between backups: "))
            else:
                self.delay = 0
            f = open("backup.config","w")
            f.write(self.dat_path + "\n" + self.backup_folder + "\n" + str(self.handle_loop) + "\n" + str(self.delay))
            f.close()
        else:
            f = open("backup.config")
            raw = f.read()
            f.close()
            split = raw.split()
            self.dat_path = str(split[0])
            self.backup_folder = str(split[1])
            self.handle_loop = int(split[2])
            self.delay = int(split[3])
        if sys.platform != "win32":
            self.s = "/"
        else:
            self.s = "\\"
        if not verify(self.backup_folder):
            os.makedirs(self.backup_folder)
        if not verify(self.backup_folder + self.s + "count"):
            f = open(self.backup_folder + self.s + "count","w")
            f.write("1")
            f.close()

    def get_count(self):
        if verify(self.backup_folder + self.s + "count"):
            f = open(self.backup_folder + self.s + "count")
            boi = int(f.read())
            f.close()
            return boi

    def save_count(self,boi):
        if verify(self.backup_folder + self.s + "count"):
            os.remove(self.backup_folder + self.s + "count")
            f = open(self.backup_folder + self.s + "count","w")
            f.write(str(boi))
            f.close()

    def backup(self):
        # shutil.copytree(src, dst)
        if verify(self.backup_folder) and verify(self.dat_path):
            if not self.handle_loop == 1:
                count = self.get_count()
                new = count + 1
                shutil.copytree(self.dat_path, self.backup_folder + self.s + "backup" + str(count))
                f = open(self.backup_folder + self.s + "backup" + str(count) + self.s + "stamp.txt","w")
                f.write("This backup is from " + str(datetime.datetime.now()))
                f.close()
                self.save_count(new)
            else:
                while True:
                    current = 0
                    while current != self.delay:
                        current += 1
                        print(str(current) + "s of " + str(self.delay) +"s\r",end="")
                        time.sleep(1)
                    current = 0
                    count = self.get_count()
                    new = count + 1
                    shutil.copytree(self.dat_path, self.backup_folder + self.s + "backup" + str(count))
                    f = open(self.backup_folder + self.s + "backup" + str(count) + self.s + "stamp.txt","w")
                    f.write("This backup is from " + str(datetime.datetime.now()))
                    f.close()
                    self.save_count(new)
                    print()
                    print("Did backup at " + str(datetime.datetime.now()))
        else:
            print("Either backup folder doesn't exist as specified, or the source folder is gone")
            print("Just delete backup.config unless you can't for some reason")
            quit()

if __name__ == "__main__":
    boi = anbackup()
    boi.backup()
