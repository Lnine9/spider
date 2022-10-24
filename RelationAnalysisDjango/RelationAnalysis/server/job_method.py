from RelationAnalysis.server.schedule_tasks import WBGtask, CBGtask, CBUtask, PUtask, AUtask, CHtask, Alltask

methods = {
    'WB_G': WBGtask,
    'CB_U': CBUtask,
    'CB_G': CBGtask,
    'PU': PUtask,
    'AU': AUtask,
    'CH': CHtask,
    'ALL': Alltask
}


def get_job_method(job_id):
    return methods.get(job_id, None)
