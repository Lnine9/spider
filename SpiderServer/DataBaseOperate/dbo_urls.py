from django.conf.urls import url

from DataBaseOperate import views

urlpatterns = [
    url(r'^add$', views.database_operate),
    url(r'^delete$', views.database_operate),
    url(r'^update$', views.database_operate),
    url(r'^query$', views.database_operate),
    url(r'^executeSql$', views.database_operate),


    url(r'^spider_model_query$', views.spider_model_query),
    url(r'^spider_await_query$', views.spider_await_query),
    url(r'^spider_await_status_query$', views.spider_await_status_query),
    url(r'^spider_init_query$', views.spider_init_query),


    url(r'^sas_update_status$', views.sas_update_status),
    url(r'^sas_update_latest_url$', views.sas_update_latest_url),
    url(r'^sas_update_crawled_section_num$', views.sas_update_crawled_section_num),
    url(r'^sas_update_aim_number$', views.sas_update_aim_number),
    url(r'^sas_update$', views.sas_update),
    url(r'^sas_update_complete_rate$', views.update_complete_rate),


    url(r'^chtml_update_section$', views.chtml_update_section),
    url(r'^chtml_update_section_neg$', views.chtml_update_section_neg),
    url(r'^chtml_query_by_spider_id$', views.chtml_query_by_spider_id),
    url(r'^chtml_query_by_id$', views.chtml_query_by_id),
    url(r'^chtml_query_section_need_delete$', views.chtml_query_section_need_delete),

    url(r'^chis_id$', views.chis_id),
    url(r'^chis_add$', views.chis_add),
    url(r'^chis_delete$', views.chis_delete),
    url(r'^chis_update$', views.chis_update),

    url(r'^uuid$', views.uuid),
    url(r'^add_dict_to_sm$', views.add_dict_to_sm),
    url(r'^query_total_num$', views.query_total_num),

    url(r'^spider_list_query$', views.spider_list_query),
    url(r'^resolver_query$', views.resolver_query),
    url(r'^resolver_update$', views.resolver_update),
    url(r'^resolver_query_by_id$', views.resolver_query_by_id),
    url(r'^sub_comp_query_by_parent$', views.sub_comp_query_by_parent),

    url(r'^rdr_query_object$', views.rdr_query_object),
    url(r'^rdr_delete_all$', views.rdr_delete_all),
    url(r'^an_delete_all$', views.an_delete_all),

    url(r'^add_an_to_db$', views.add_an_to_db),

    url(r'^query_latest_url$', views.query_latest_url),


    url(r'^dis_group$', views.dis_group),
    url(r'^client_update$', views.client_update),

    url(r'^sas_update_spider_await_status$', views.sas_update_spider_await_status),
]


