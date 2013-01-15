import sys, sublime, sublime_plugin, time, datetime, os, threading, subprocess, re, Queue
exe = __import__('exec')

class KeepTestingCommand(sublime_plugin.EventListener):
    success_pattern = re.compile('BUILD SUCCESSFUL')
    fail_pattern = re.compile('(\d+) tests completed, (\d+) failed')

    running_tests = []
    lock_path = None
    project_path = None
    test_results = Queue.Queue()

    def run_tests(self):
        self.project_path = sublime.active_window().folders()[0]
        self.lock_path = self.project_path + "/.keepTestingLock"
        if self.is_running() == False:
            self.start_tests()
            self.check_results()

    def check_results(self):
        if (self.test_results.empty() == False):
            result = self.test_results.get(False)
            if (result == 0):
                sublime.status_message("All tests OK")
            elif (result == -1):
                sublime.status_message("Unexpected error during tests, see console")
            else:
                sublime.status_message(str(result) + " tests failed")
        else:
            #print str(datetime.datetime.now()) + " - queue empty, still running?"
            sublime.set_timeout(self.check_results, 200)


    def stopped_tests(self):
        if self.lock_path is None:
            print "Error: lock_path not set"
            return
        if self.is_running():
            #print "stopping tests"
            os.unlink(self.lock_path)

    def start_tests(self):
        if self.lock_path is None:
            print "Error: lock_path not set"
            return
        #print "starting tests"
        self.test_results = Queue.Queue()
        threading.Thread(target=self.worker, args=(self.test_results,)).start()
        with open (self.lock_path, 'w') as f: f.write('')

    def is_running(self):
        if self.lock_path is None:
            print "Error: lock_path not set"
            return false
        return os.path.isfile(self.lock_path)

    def worker(self, result):
        #print "worker starting with lock_path " + self.lock_path
        p = subprocess.Popen(['/usr/local/bin/gradle', '--daemon', 'clean', 'test'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.project_path)
        out = ''
        failed_tests = None
        while(True):
            retcode = p.poll()
            line = p.stdout.readline()
            out += line
            #print ":::" + line
            if KeepTestingCommand.success_pattern.match(line):
                failed_tests = 0
            else:
                m = KeepTestingCommand.fail_pattern.match(line)
                if m:
                    failed_tests = m.group(2)
            if (retcode is not None):
                break
        if (failed_tests is None):
            result.put(-1)
            print out
        else:
            result.put(failed_tests)
        self.stopped_tests()
        return

    def on_post_save(self, view):
        sublime.set_timeout(self.run_tests, 1)

