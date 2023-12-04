from dataclasses import dataclass
from threading import (
    BoundedSemaphore,
    Condition,
    Lock,
    RLock,
    Semaphore,
    Thread,
)
from unittest import main, TestCase

from door.multiprocessing2 import Handle
from door.primitives import Acquirable, SAcquirable, SWaitable, Waitable
from door.threading2 import (
    AcquirableDoor,
    RSCondition,
    RSLock,
    SAcquirableDoor,
    SWaitableDoor,
    WaitableDoor,
    WSCondition,
    WSLock,
)


class ThreadingTestCase(TestCase):
    @dataclass
    class Resource:
        key: str = 'value'

    @dataclass
    class Flags:
        ready: bool = False
        processed: bool = False

    @dataclass
    class Counter:
        value: int = 0

    def test_unhandled(self) -> None:
        handle = Handle(None)

        self.assertRaises(ValueError, AcquirableDoor, handle, Lock())
        handle.unlink()

    def test_acquirable(self) -> None:
        for primitive in (
                Lock(),
                RLock(),
                Condition(),
                Semaphore(),
                BoundedSemaphore(),
        ):
            assert isinstance(primitive, Acquirable)

            resource = self.Resource()
            door = AcquirableDoor(resource, primitive)

            with door() as proxy:
                self.assertEqual(proxy.key, 'value')
                proxy.key = 'VALUE'
                self.assertEqual(proxy.key, 'VALUE')

            self.assertRaises(ValueError, getattr, proxy, 'key')
            self.assertRaises(ValueError, setattr, proxy, 'key', 'value')
            self.assertEqual(resource, self.Resource('VALUE'))

    def test_waitable(self) -> None:
        def worker() -> None:
            with door() as proxy:
                while not proxy.ready:
                    door.wait()

                proxy.processed = True

                door.notify()

        for primitive in (
                Condition(),
        ):
            assert isinstance(primitive, Waitable)

            resource = self.Flags()
            door = WaitableDoor(resource, primitive)
            thread = Thread(target=worker)

            thread.start()

            with door() as proxy:
                proxy.ready = True

                door.notify()

            with door() as proxy:
                while not proxy.processed:
                    door.wait()

                self.assertTrue(proxy.processed)

            thread.join()

    def test_shared_acquirable_0(self) -> None:
        for primitive in (
                RSLock(),
                WSLock(),
                RSCondition(),
                WSCondition(),
        ):
            assert isinstance(primitive, SAcquirable)

            resource = self.Resource()
            door = SAcquirableDoor(resource, primitive)

            with door.read() as proxy:
                self.assertEqual(proxy.key, 'value')
                self.assertRaises(ValueError, setattr, proxy, 'key', 'VALUE')

            with door.write() as proxy:
                self.assertEqual(proxy.key, 'value')
                proxy.key = 'VALUE'
                self.assertEqual(proxy.key, 'VALUE')

            self.assertRaises(ValueError, getattr, proxy, 'key')
            self.assertRaises(ValueError, setattr, proxy, 'key', 'value')
            self.assertEqual(resource, self.Resource('VALUE'))

    def test_shared_acquirable_1(self) -> None:
        ITER_COUNT = 1000
        PARALLELISM_COUNT = 10

        def read() -> int:
            with door.read() as proxy:
                return proxy.value

        def write() -> None:
            with door.write() as proxy:
                proxy.value += 1

        def target() -> None:
            for _ in range(ITER_COUNT):
                write()
                read()

        for primitive in (
                RSLock(),
                WSLock(),
                RSCondition(),
                WSCondition(),
        ):
            assert isinstance(primitive, SAcquirable)

            counter = self.Counter()
            door = SAcquirableDoor(counter, primitive)
            threads = []

            for _ in range(PARALLELISM_COUNT):
                thread = Thread(target=target)

                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            self.assertEqual(counter.value, ITER_COUNT * PARALLELISM_COUNT)

    def test_shared_waitable(self) -> None:
        def worker() -> None:
            with door.write() as proxy:
                while not proxy.ready:
                    door.wait_write()

                proxy.processed = True

                door.notify_write()

        for primitive in (
                RSCondition(),
                WSCondition(),
        ):
            assert isinstance(primitive, SWaitable)

            resource = self.Flags()
            door = SWaitableDoor(resource, primitive)
            thread = Thread(target=worker)

            thread.start()

            with door.write() as proxy:
                proxy.ready = True

                door.notify_write()

            with door.read() as proxy:
                while not proxy.processed:
                    door.wait_read()

                self.assertTrue(proxy.processed)

            thread.join()


if __name__ == '__main__':
    main()  # pragma: no cover
