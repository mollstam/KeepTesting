import sys, sublime, sublime_plugin, time, datetime, os, threading, subprocess, re, multiprocessing
exe = __import__('exec')

class KeepTestingCommand(sublime_plugin.EventListener):
    test_status_pattern = re.compile('.*\[TestEventLogger\] ([A-Za-z0-9\._]+) > ([A-Za-z0-9_]+) ([A-Z]+).*')

    test_runs = []
    running_tests = []
    lock_path = None
    project_path = None
    test_results = multiprocessing.Manager().dict()
    done = False
    stop = False

    def run_tests(self):
        KeepTestingCommand.test_runs.append(self)
        self.done = False
        self.project_path = sublime.active_window().folders()[0]
        self.lock_path = self.project_path + "/.keepTestingLock"
        if self.is_running() == False:
            self.start_tests()
            self.check_results()

    def stop_all(self):
        for t in KeepTestingCommand.test_runs:
            t.stop = True

    def check_results(self):
        if self.stop:
            return

        if self.done and self.is_running():
            return

        if (len(self.test_results.keys()) != 0):
            progressbar = "["
            error_message = ""
            keys = self.test_results.keys()
            test_count = 0
            test_ok = 0
            test_fail = 0
            for k in keys:
                test_count += 1
                result = self.test_results[k]
                if (result == 'PASSED'):
                    test_ok += 1
                    progressbar += '-'
                elif (result == 'FAILED'):
                    test_fail += 1
                    progressbar += 'X'
                    error_message = k
                elif (result == 'STARTED'):
                    progressbar += 'o'
                else:
                    print "Unknown result for " + k + ": " + result
                    progressbar += '?'
            progressbar += "] " + str(test_ok)  + "/" + str(test_count) + " passed"
            if test_fail > 0:
                progressbar += " - FAIL " + error_message
            sublime.status_message(progressbar)

        if self.is_running() or test_fail > 0:
            sublime.set_timeout(self.check_results, 50)


    def stopped_tests(self):
        if self.lock_path is None:
            print "Error: lock_path not set"
            return
        if self.is_running():
            #print "stopping tests"
            os.unlink(self.lock_path)
            self.done = True

    def start_tests(self):
        if self.lock_path is None:
            print "Error: lock_path not set"
            return
#        print "starting tests"
        sublime.status_message("Running tests...")
        with open (self.lock_path, 'w') as f: f.write('')
        self.test_results = multiprocessing.Manager().dict()
        threading.Thread(target=self.worker, args=(self.test_results,)).start()

    def is_running(self):
        if self.lock_path is None:
            print "Error: lock_path not set"
            return false
        return os.path.isfile(self.lock_path)

    def worker(self, result):
        p = subprocess.Popen(['/usr/local/bin/gradle', '--daemon', '--debug', 'clean', 'test'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.project_path)
        out = ''
        success = False
        failed_tests = None
        while(True):
            retcode = p.poll()
            line = p.stdout.readline()
            out += line
            m = KeepTestingCommand.test_status_pattern.match(line)
            if m:
                result[m.group(1) + " : " + m.group(2)] = m.group(3)
            if (retcode is not None):
                break
        self.stopped_tests()
        return

    def on_post_save(self, view):
        if (len(sublime.active_window().folders()) == 0):
            self.stop_all()
            return

        if (os.path.isdir(sublime.active_window().folders()[0] + "/.gradle") == False):
            self.stop_all()
            return

        if '..' in os.path.relpath(view.file_name(), sublime.active_window().folders()[0]):
            self.stop_all()
            return

        cmd = KeepTestingCommand()
        sublime.set_timeout(cmd.run_tests, 1)

