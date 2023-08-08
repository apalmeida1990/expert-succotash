# Technical Description

## The Problem

Managing the data flows like the ones requested in the goals above requires a strong DevOps
component.

Please discuss what strategies, technologies and tools you would use to simplify and automate
this day to day management, namely:

- metrics and monitoring for the running dataflows
- recovering from a failed dataflow
- testing a dataflow in a development environment and then deploying it to a production environment
- modifying code on the dataflow without stopping it

## Summary

This document will offer a discussion about the strategies, technologies and tools that can be used to simplify and automate the management of the data flows.

As refered on the interview, I'm not an expert on DevOps. However, I have some experience with some topics. I will try to provide the best solution based on my experience and knowledge. Some of the topics I'll be discussing are:

- Monitoring
- Infrastructure Deployment
- Continuous Integration and Continuous Deployment

## Discussion

### Monitoring

This topic was already discussed in the previous exercise. Please refer to the [Monitoring](../ex_3/README.md#monitoring) section of the previous exercise. However, I will add some more information here.

1. Google Cloud Logging:
   - **Logs Explorer**: Allow to search for logs across projects, resources, and time. You can filter the logs by severity, resource, project, etc. You can also create alerts based on the logs.
   - **Export to BigQuery**: Allow to export the logs to BigQuery. This way you can query the logs using SQL and create dashboards with the logs.
2. Google Cloud Monitoring:
   - **Custom Dashboards**: Allow to create custom dashboards with the metrics that we want to monitor. We can create dashboards for each dataflow, for each team, for each project, etc. Provide a real-time view of the metrics.
   - **Alerting**: You can create alerts based on the metrics that you want to monitor. For example, when the RAM, CPU or Disk usage reach a specific threshold, you can trigger an alert to notify you.
   - **Integration with logging**: You can integrate the metrics with the logs. For example, you can create a dashboard with the number of errors that occurred in the last 24 hours and the logs of those errors.

You can also use tools like **Prometheus** and **Grafana** if you aren't using managed service by Google Cloud Platform.

### Infrastructure Deployment

For infrastructure deployment, I am all for **Infrastructure as Code**. My preference goes to **Terraform**. Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Terraform can manage existing and popular service providers as well as custom in-house solutions.

Terraform allows you to reduce the downtime of your services by doing a rolling update of your infrastructure. You can also use Terraform to create a new environment, like a staging environment, and then promote it to production.

In the solution proposed, not all the components would be deployed using Terraform. For example, the **Cloud Functions** will be deployed using Cloud SDK (gcloud) on CI/CD pipelines because they are very dependent on the code that you are writing. They need to be deployed every time a merge is done on the repository.

### Continuous Integration and Continuous Deployment

Although you have tools like Jenkins, my preference goes to **Gitlab CI/CD** or **Github Actions**. Mainly because Gitlab and Github are the most adopted git repository managers which is most of the cases gives a quick integration with the CI/CD tools.

I won't discuss here which git flow (Gitflow, Github Flow, Gitlab Flow, trunk-based development, etc) you should use. I will assume that you already have a git flow in place.

For sake of simplicity, let's assume we have:

| Branch | Environment Name |
| ----------- | ----------- |
| master | production |
| develop | staging |

Some of the pipelines that I would create are:

1. **Pull Request Pipeline**: This pipeline will run when a pull request is created.
   1. It will run the unit tests (not data quality tests) and the linters. If the tests and linters pass, it will allow the pull request to be merged after the approval of the reviewers.
   2. Ideally, you want to execute the new code before allowing the pull request to be merged. However, from my experience, sometimes this is hard to achieve because you need to create a new environment for each pull request. Some reasons that I found to be recurrent for this pipeline don't exist are:
      1. Too many pull requests are created at the same time. This will create a bottleneck in the infrastructure, specially if you are using a managed service like Google Cloud Platform. This will increase the cost of the infrastructure quickly.
      2. You can try to launch a new Kubernetes pod in a cluster made for this purpose. The pod is destroyed as soon as the pipeline finishes. However, this will require that you build a container that contains all the services that you are currently using.
         1. Currently, data team uses many cloud services like BigQuery, Dataflow, Pub/Sub, etc. You will need to create a container that contains all these services or something similar.
            1. For example, for AWS you can use [localstack](https://docs.localstack.cloud/overview/) to mock the AWS services.
            2. For BigQuery, you don't have a similar alternative. You might need to use a difference database like PostgreSQL. An alternative that is very popular currently is DuckDB. DuckDB is an embeddable SQL OLAP database management system. It is designed to be run inside applications as an embedded database, supporting OLAP and OLTP use cases.
         2. You need to build you seed data. The goal is to run **Data Quality Tests** using always the same input data.
            1. This might be difficult to achieve if your data model is already too complex
   3. If you are able to introduce the point above in you CI/CD pipeline, you can then run the **Data Quality Tests**. The pipeline will be fully executed and only then the tests will be executed. If the tests pass, the pull request will be merged. You can use libraries like [Great Expectations](https://greatexpectations.io/) to create the data quality tests.
      1. You'll be able to detect problems like duplicate data, missing data, etc.

2. **Staging Pipeline**: This pipeline will run when a commit is pushed to the develop branch (or you merge a pull request to the develop branch). The expected actions are:
   1. Deploy any code dependent services like **Cloud Functions**.
   2. In this pipeline you want to run **Integration Tests** using the data that you have in the staging environment. You can use the same libraries that you used in the previous pipeline. You can also trigger any other test pipeline that you have.

3. **Production Pipeline**: This pipeline will run when a commit is pushed to the master branch (or you merge a pull request to the master branch). Here the expected actions are more or less the same as the staging pipeline. The difference is that you will use the production data to run the tests.

### Other topics

Below, a list of topics that I think are important to discuss when designing a data platform but because lack of time I won't discuss here.

1. **Security and Compliance**
   - **Data encryption**
   - **Identity and Access Management (IAM)**
   - **GDPR, HIPAA, etc**

2. Disaster Recovery and High Availability
   - **Multi-region** and **zone** deployments. For example, if a full region goes down, you can still have your services running in another region.
   - **Backup strategies**. Beside the traditional ones, like backup to a different region, in more mature organizations you might consider multi-cloud backup. For example, you can backup your data from AWS S3 to Google Cloud Storage and vice-versa.

3. Data Governance
   - **Data Catalog**: A data catalog is a metadata management tool designed to help organizations find and manage large amounts of data – including tables, files, and databases – stored in their ERP, human resources, finance, and other systems and business applications.
   - **Data Lineage**: Data lineage is the process of tracking data from its origin to its destination. It is the process of understanding the flow of your data. It is important to understand the data lineage to understand the impact of a change in a data source.
   - **Data Quality**: Data quality is the process of understanding the quality of your data. It is important to understand the quality of your data to understand the impact of a change in a data source.
