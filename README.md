## AWS ParallelCluster serverless API for AWS Batch

This code of this repository is a continuation of a series that demostrates how to create serverless architectures to support HPC workloads run with AWS ParallelCluster. The first post in this series, Using AWS ParallelCluster with a serverless API, (https://aws.amazon.com/blogs/compute/using-aws-parallelcluster-with-a-serverless-api/) explained how to create a serverless API for the AWS ParallelCluster command line interface. The second post, AWS API Gateway for HPC job submission (https://aws.amazon.com/blogs/opensource/aws-api-gateway-hpc-job-submission/), explained how to submit jobs to a cluster that uses a Slurm job scheduler through a similar serverless API. In this post we combine AWS ParallelCluster (https://github.com/aws/aws-parallelcluster), AWS API Gateway (https://aws.amazon.com/api-gateway/) and AWS Lambda (https://aws.amazon.com/lambda/) to make a serverless API of the AWS Batch command line interface inside ParallelCluster. 

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

