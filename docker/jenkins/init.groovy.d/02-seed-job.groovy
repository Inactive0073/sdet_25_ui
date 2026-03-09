import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

def instance = Jenkins.get()
def jobName = System.getenv("JENKINS_SEED_JOB_NAME") ?: "bankingproject-ui-tests"
def pipelineFile = new File("/workspace/Jenkinsfile")

if (!pipelineFile.exists()) {
    println("Pipeline file not found: ${pipelineFile.absolutePath}")
    return
}

WorkflowJob job = instance.getItem(jobName)
if (job == null) {
    job = instance.createProject(WorkflowJob, jobName)
}

job.setDefinition(new CpsFlowDefinition(pipelineFile.text, true))
job.save()
instance.save()

println("Seeded Jenkins pipeline job: ${jobName}")
