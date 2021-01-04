
from pytest import raises
from upsolve.main import UpsolveTest

def test_upsolve():
    # test upsolve without any subcommands or arguments
    with UpsolveTest() as app:
        app.run()
        assert app.exit_code == 0


def test_upsolve_debug():
    # test that debug mode is functional
    argv = ['--debug']
    with UpsolveTest(argv=argv) as app:
        app.run()
        assert app.debug is True


def test_command1():
    # test command1 without arguments
    argv = ['command1']
    with UpsolveTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'bar'
        assert output.find('Foo => bar')


    # test command1 with arguments
    argv = ['command1', '--foo', 'not-bar']
    with UpsolveTest(argv=argv) as app:
        app.run()
        data,output = app.last_rendered
        assert data['foo'] == 'not-bar'
        assert output.find('Foo => not-bar')
