from transformers.trainer_callback import ProgressCallback

from .training_master_client import TrainingMasterClient

_client = TrainingMasterClient()


class ProgressReport(ProgressCallback):
    """
    usage:
        from megamind_sdk.api.progress_report import ProgressReport

        trainer = Trainer(...)
        trainer.add_callback(ProgressReport)
    """

    def on_step_end(self, args, state, control, **kwargs):
        _ = self
        if state.is_local_process_zero:
            _client.progress_report(state.global_step, state.max_steps)

    @staticmethod
    def set_report_interval(report_interval: int):
        """
        report interval percentage [1-100]
        """

        report_interval = 1 if report_interval < 0 else report_interval
        _client.job_metadata["notice_interval"] = report_interval

