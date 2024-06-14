import subprocess
import shutil
import pytest

from facefusion.typing import Args
from facefusion.download import conditional_download
from facefusion.jobs.job_manager import init_jobs, clear_jobs, create_job, submit_job, submit_jobs, add_step
from facefusion.jobs.job_runner import run_job, run_jobs, run_steps, finalize_steps, collect_output_set
from .helper import get_test_jobs_directory, get_test_examples_directory, get_test_example_file, get_test_output_file, prepare_test_output_directory, is_test_output_file


@pytest.fixture(scope = 'module', autouse = True)
def before_all() -> None:
	conditional_download(get_test_examples_directory(),
	[
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/source.jpg',
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/target-240p.mp4'
	])
	subprocess.run([ 'ffmpeg', '-i', get_test_example_file('target-240p.mp4'), '-vframes', '1', get_test_example_file('target-240p.jpg') ])


@pytest.fixture(scope = 'function', autouse = True)
def before_each() -> None:
	clear_jobs(get_test_jobs_directory())
	init_jobs(get_test_jobs_directory())
	prepare_test_output_directory()


def process_step(step_args : Args) -> bool:
	return shutil.copy(step_args.get('target_path'), step_args.get('output_path'))


def test_run_job() -> None:
	args_1 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-1.mp4')
	}
	args_2 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-2.mp4')
	}
	args_3 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.jpg'),
		'output_path': get_test_output_file('output-1.jpg')
	}

	assert run_job('job-test-run-job', process_step) is False

	create_job('job-test-run-job')
	add_step('job-test-run-job', args_1)
	add_step('job-test-run-job', args_2)
	add_step('job-test-run-job', args_2)
	add_step('job-test-run-job', args_3)

	assert run_job('job-test-run-job', process_step) is False

	submit_job('job-test-run-job')

	assert run_job('job-test-run-job', process_step) is True


def test_run_jobs() -> None:
	args_1 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-1.mp4')
	}
	args_2 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-2.mp4')
	}
	args_3 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.jpg'),
		'output_path': get_test_output_file('output-1.jpg')
	}

	assert run_jobs(process_step) is False

	create_job('job-test-run-jobs-1')
	create_job('job-test-run-jobs-2')
	add_step('job-test-run-jobs-1', args_1)
	add_step('job-test-run-jobs-1', args_1)
	add_step('job-test-run-jobs-2', args_2)
	add_step('job-test-run-jobs-3', args_3)

	assert run_jobs(process_step) is False

	submit_jobs()

	assert run_jobs(process_step) is True


@pytest.mark.skip()
def test_retry_job() -> None:
	pass


@pytest.mark.skip()
def test_retry_jobs() -> None:
	pass


def test_run_steps() -> None:
	args_1 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-1.mp4')
	}
	args_2 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-2.mp4')
	}
	args_3 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.jpg'),
		'output_path': get_test_output_file('output-1.jpg')
	}

	assert run_steps('job-run-steps', process_step) is False

	create_job('job-run-steps')
	add_step('job-run-steps', args_1)
	add_step('job-run-steps', args_1)
	add_step('job-run-steps', args_2)
	add_step('job-run-steps', args_3)

	assert run_steps('job-run-steps', process_step) is True


def test_finalize_steps() -> None:
	args_1 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-1.mp4')
	}
	args_2 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-2.mp4')
	}
	args_3 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.jpg'),
		'output_path': get_test_output_file('output-1.jpg')
	}

	create_job('job-finalize-steps')
	add_step('job-finalize-steps', args_1)
	add_step('job-finalize-steps', args_1)
	add_step('job-finalize-steps', args_2)
	add_step('job-finalize-steps', args_3)

	shutil.copy(args_1.get('target_path'), get_test_output_file('output-1-job-finalize-steps-0.mp4'))
	shutil.copy(args_1.get('target_path'), get_test_output_file('output-1-job-finalize-steps-1.mp4'))
	shutil.copy(args_2.get('target_path'), get_test_output_file('output-2-job-finalize-steps-2.mp4'))
	shutil.copy(args_3.get('target_path'), get_test_output_file('output-1-job-finalize-steps-3.jpg'))

	assert finalize_steps('job-finalize-steps') is True
	assert is_test_output_file('output-1.mp4') is True
	assert is_test_output_file('output-2.mp4') is True
	assert is_test_output_file('output-1.jpg') is True


def test_collect_output_set() -> None:
	args_1 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-1.mp4')
	}
	args_2 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.mp4'),
		'output_path': get_test_output_file('output-2.mp4')
	}
	args_3 =\
	{
		'source_path': get_test_example_file('source.jpg'),
		'target_path': get_test_example_file('target-240p.jpg'),
		'output_path': get_test_output_file('output-1.jpg')
	}

	create_job('job-collect-output-set')
	add_step('job-collect-output-set', args_1)
	add_step('job-collect-output-set', args_1)
	add_step('job-collect-output-set', args_2)
	add_step('job-collect-output-set', args_3)

	output_set =\
	{
		get_test_output_file('output-1.mp4'):
		[
			get_test_output_file('output-1-job-collect-output-set-0.mp4'),
			get_test_output_file('output-1-job-collect-output-set-1.mp4')
		],
		get_test_output_file('output-2.mp4'):
		[
			get_test_output_file('output-2-job-collect-output-set-2.mp4')
		],
		get_test_output_file('output-1.jpg'):
		[
			get_test_output_file('output-1-job-collect-output-set-3.jpg')
		]
	}

	assert collect_output_set('job-collect-output-set') == output_set