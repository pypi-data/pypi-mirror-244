from transformers.trainer_callback import ProgressCallback

from .training_master_client import TrainingMasterClient

_client = TrainingMasterClient()


class ProgressReport(ProgressCallback):
    def on_step_end(self, args, state, control, **kwargs):
        _ = self
        if state.is_local_process_zero:
            _client.progress_report(int(state.global_step / state.max_steps), state.max_steps)
