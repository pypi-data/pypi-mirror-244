from google.cloud import run_v2
from google.cloud import monitoring_v3
from . import gcp_utils, tools
import statistics, time, json

def get_run_service(service=None, project_id=None, region=None):
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    service_id = f"projects/{project_id}/locations/{region}/services/{service}"
    run_client = run_v2.ServicesClient()
    run_service = run_client.get_service(name=service_id)
    return run_service

def get_run_revision(revision=None, service=None, project_id=None, region=None):
    if revision == None:
        revision = gcp_utils.get_revision_id()

    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    revision_id = f"projects/{project_id}/locations/{region}/services/{service}/revisions/{revision}"
    run_client = run_v2.RevisionsClient()
    run_revision = run_client.get_revision(name=revision_id)

    return run_revision

def get_latest_revision(service=None, project_id=None, region=None):
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_service = get_run_service(service=service, project_id=project_id, region=region)
    service_revision = gcp_utils.get_resource_from_path(run_service.latest_ready_revision)
    return service_revision

def get_service_url(service=None, project_id=None, region=None):
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_service = get_run_service(service=service, project_id=project_id, region=region)
    return run_service.uri

def get_last_update_ts(service=None, project_id=None, region=None):
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_service = get_run_service(service=service, project_id=project_id, region=region)
    return tools.get_pacific_timestamp(run_service.update_time)

def get_instance_count(service=None, project_id=None, region=None):
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    monitoring_metric = "run.googleapis.com/container/instance_count"
    aggregation_s = 60
    interval_s = 240 # Instance count reporting delay up to 180s (errors with just 180)

    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": {"seconds": seconds, "nanos": nanos},
            "start_time": {"seconds": (seconds - interval_s), "nanos": nanos},
        }
    )

    aggregation = monitoring_v3.Aggregation(
        {
            "alignment_period": {"seconds": aggregation_s},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
            "cross_series_reducer": monitoring_v3.Aggregation.Reducer.REDUCE_MAX,
            "group_by_fields": ["resource.labels.service_name"],
        }
    )

    metric_request = monitoring_v3.ListTimeSeriesRequest(
    name=project_name,
    filter=f'metric.type = "{monitoring_metric}" AND resource.labels.service_name = "{service}"',
    interval=interval,
    view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    aggregation=aggregation,
)

    results = client.list_time_series(request=metric_request)
    metric_data = []

    for data_point in results.time_series[0].points:
        metric_value = data_point.value.double_value
        metric_data_point = metric_value
        metric_data.append(metric_data_point)
        
    return_val = round(statistics.fmean(metric_data))
    return return_val

def get_service_min_instances(service=None, project_id=None, region=None, access_token=None):
    # Get service-level min-instances setting
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()
    run_service = gcp_utils.call_admin_api(path=f'services/{service}', 
                                url='https://run.googleapis.com/v2',
                                op="GET", 
                                project_id=project_id,
                                region=region,
                                access_token=access_token
                                )
    
    try:
        min_instances = run_service['scaling']['minInstanceCount']
    except:
        print("Error reading Service Min Instances")
        min_instances = 0

    return min_instances

def set_service_min_instances(instances, service=None, project_id=None, region=None, access_token=None):
    # Manually change Run instance count (via Service-level min-instances)
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_service = gcp_utils.call_admin_api(path=f'services/{service}', 
                                url='https://run.googleapis.com/v2',
                                op="GET",
                                project_id=project_id,
                                region=region,
                                access_token=access_token
                                )
    run_service['scaling']['minInstanceCount'] = instances
    op_response = gcp_utils.call_admin_api(path=f'services/{service}', 
                                url='https://run.googleapis.com/v2',
                                op="PATCH",
                                payload=json.dumps(run_service),
                                project_id=project_id,
                                region=region,
                                access_token=access_token
                                )
    
    return op_response

def get_revision_max_instances(revision=None, service=None, project_id=None, region=None, access_token=None):
    # Get revision-level max-instances setting
    if revision == None:
        revision = gcp_utils.get_revision_id()
    
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_revision = gcp_utils.call_admin_api(path=f'services/{service}/revisions/{revision}', 
                                url='https://run.googleapis.com/v2',
                                op="GET", 
                                project_id=project_id,
                                region=region,
                                access_token=access_token
                                )
    
    try:
        max_instances = run_revision['scaling']['maxInstanceCount']
    except:
        print("Error reading Revision Max Instances")
        max_instances = 0

    return max_instances

def get_revision_min_instances(revision=None, service=None, project_id=None, region=None, access_token=None):
    # Get revision-level min-instances setting
    if revision == None:
        revision = gcp_utils.get_revision_id()
    
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_revision = gcp_utils.call_admin_api(path=f'services/{service}/revisions/{revision}', 
                                url='https://run.googleapis.com/v2',
                                op="GET", 
                                project_id=project_id,
                                region=region,
                                access_token=access_token
                                )
    
    try:
        min_instances = run_revision['scaling']['minInstanceCount']
    except:
        print("Error reading Revision Min Instances")
        min_instances = 0

    return min_instances

def get_revision_max_concurrency(revision=None, service=None, project_id=None, region=None, access_token=None):
    # Get revision-level max-concurrency setting
    if revision == None:
        revision = gcp_utils.get_revision_id()
    
    if service == None:
        service = gcp_utils.get_service_id()

    if project_id == None:
        project_id = gcp_utils.get_project_id()
    
    if region == None:
        region = gcp_utils.get_gcp_region()

    run_revision = get_run_revision(revision=revision, service=service, project_id=project_id, region=region, access_token=access_token)
    
    try:
        max_concurrency = run_revision.max_instance_request_concurrency
    except:
        print("Error reading Revision Max Concurrency")
        max_concurrency = None

    return max_concurrency