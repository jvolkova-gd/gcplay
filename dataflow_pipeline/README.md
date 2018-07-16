### Few steps to start work with GCP

To start work with Google Cloud from you local machine first 
of all read about gcloud command line and download it:

    https://cloud.google.com/sdk/docs/ 

#### Run Dataflow job
In BeamDriver.java change default settings to your project and cloud bucket:

    @Default.String("gs://hybrid-elysium-118418/dataflow/output.txt")
    
    and 
    
    @Default.String("projects/hybrid-elysium-118418/topics/botgen")

Before run jar run from terminal gcloud command to auth in platform:

    gcloud auth application-default login
    
After what run this command, you need to change --project to your project name:

    mvn compile exec:java -Dexec.mainClass=xnuinside.beam_playground.BeamDriver 
    -Dexec.args="--project=hybrid-elysium-118418 --runner=DataflowRunner"


####How to delete a gcloud Dataflow job?

It is not possible to delete Dataflow jobs. However, note that 
you can filter the job list to only show the jobs you care about. 
For example, Status:Running,Succeeded
