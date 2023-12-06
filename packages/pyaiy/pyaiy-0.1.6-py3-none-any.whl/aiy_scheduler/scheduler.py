

import typing
import uuid
from threading import Thread, Lock
import time
from enum import Enum
from queue import Empty, Queue

from aiy_log import logger

class SchedulerRequest:
    req_id: str
    ''' Task ID'''

    def __init__(self, id):
        self.req_id = id

class Task:
    '''
    Task

    继承此抽象类来编写具体任务及其 Handler

    Attributes
    -----------
    id: str | None
        任务唯一 ID
    
    Example
    ---
    ```python
    class TTSTask(Task):
        role: str
        text: str
        output: str

        def __init__(self, role, text) -> None:
            self.role = role
            self.text = text
            self.output = 'output.wav'
            super()

        def run(self):
            if self.id:
                self.output = f'{OUTPUTS}/{self.id}.wav'
            # real work
            tts(self)

    ```
    '''
    id: str | None

    def __init__(self) -> None:
        pass
    
    def run(self) -> None:
        raise Exception('not implemented')

class TaskStatus(Enum):
    Prepare = 1
    Running = 2
    Finished = 3
    Fatal = 4

    def __str__(self) -> str:
        return self.name

class TaskWithId:
    id: str
    task: Task
    status: TaskStatus
    start_at: float

    def __init__(self, id: str, task: Task) -> None:
        self.id = id
        self.task = task
        self.task.id = id
        self.status = TaskStatus.Prepare
        self.start_at = time.time()

class Scheduler:
    '''
    Scheduler 调度器

    Example:
    ---
    ```python
    # init scheduler
    scheduler = Scheduler()
    scheduler.async_run()

    # ...
    req = scheduler.submit_task(task)
    print(req.req_id)

    # check the task's status
    task = scheduler.check_status(id)
    print(task.status)
    ```
    '''
    tasks: typing.Dict[str, TaskWithId]
    '''任务记录'''
    tasks_mutex: Lock
    '''同步锁'''
    q: Queue
    '''任务队列'''
    running: bool
    '''是否有任务在运行'''
    thread: Thread
    '''异步线程'''
    queue_size: int
    '''缓存队列容量'''

    def __init__(self, queue_size=100) -> None:
        self.tasks = {}
        self.running = False
        self.queue_size = queue_size
        self.q = Queue(maxsize=self.queue_size)
        self.tasks_mutex = Lock()
    
    def submit_task(self, task: Task) -> SchedulerRequest:
        '''提交任务'''
        if self.q.full():
            raise Exception('Tasks queue is full')
        id = str(uuid.uuid4())
        t = TaskWithId(id, task)
        self.q.put(t)
        self.tasks_mutex.acquire()
        self.tasks[id] = t
        self.tasks_mutex.release()
        return SchedulerRequest(id)

    def check_status(self, id: id) -> TaskWithId | None:
        '''检查任务状态'''
        self.tasks_mutex.acquire()
        if id in self.tasks:
            self.tasks_mutex.release()
            return self.tasks[id]
        self.tasks_mutex.release()
        return None

    def close(self):
        print("Warm shutdown...")
        self.tasks_mutex.acquire()
        self.running = False
        self.tasks_mutex.release()

    def __run(self):
        while True:
            # check is running
            self.tasks_mutex.acquire()
            if not self.running:
                self.tasks_mutex.release()
                break
            self.tasks_mutex.release()
            try:
                # 需设置超时，否则当执行到此时，线程卡住，则无法判断当前 scheduler 是否已关闭
                task: TaskWithId = self.q.get(timeout=1.)
            except Empty:
                continue
            if task.id not in self.tasks:
                continue
            logger.info(f'Get new task: {task.id}')
            try:
                self.tasks_mutex.acquire()
                self.tasks[task.id].status = TaskStatus.Running
                self.tasks[task.id].start_at = time.time()
                self.tasks_mutex.release()
                task.task.run()
                self.tasks_mutex.acquire()
                self.tasks[task.id].status = TaskStatus.Finished
                self.tasks_mutex.release()
                logger.info(f'Task {task.id} is done')
            except Exception as e:
                logger.error(f'Task {task.id} is Fatal: {e}')
                self.tasks_mutex.acquire()
                self.tasks[task.id].status = TaskStatus.Fatal
                self.tasks_mutex.release()
            finally:
                time.sleep(1)

    def async_run(self):
        '''异步运行调度器（将在异步线程中运行）'''
        if self.running:
            return
        # 启动一个异步线程运行 tasks
        try:
            self.thread = Thread(target=self.__run)
            self.running = True
            self.thread.start()
        except Exception as e:
            self.running = False
            print(e)            
