package xnuinside.beam_playground;

import org.apache.beam.runners.dataflow.options.DataflowPipelineOptions;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;

import org.apache.beam.runners.dataflow.DataflowRunner;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.windowing.FixedWindows;
import org.apache.beam.sdk.transforms.windowing.Window;
import org.apache.beam.sdk.io.gcp.pubsub.PubsubIO;
import org.joda.time.Duration;
import org.joda.time.Instant;

/*
 --runner=BlockingDataflowPipelineRunner
   *        --project=[dataflow project] \\
   *        --stagingLocation=gs://[your google storage bucket] \\
   *        --bigtableProjectId=[bigtable project] \\
   *        --bigtableInstanceId=[bigtable instance id] \\
   *        --bigtableTableId=[bigtable tableName]
   *        --inputFile=[file path on GCS]
   *        --pubsubTopic=projects/[project name]/topics/[topic name]
 */
public class BeamDriver {

    public interface BotDataFlowOptions extends PipelineOptions{

        @Description("Pub/Sub IO settings")
        @Default.String("projects/hybrid-elysium-118418/topics/botgen")
        String getPubsubTopic();
        void setPubsubTopic(String value);

        @Default.Integer(10)
        Integer getWindowSize();
        void setWindowSize(Integer value);

        @Default.String("gs://hybrid-elysium-118418/dataflow/output.txt")
        String getOutput();
        void setOutput(String value);

    }

    static class ExtractWordsFn extends DoFn<String, String> {
        private static final long serialVersionUID = 0;

        @DoFn.ProcessElement
        public void processElement(ProcessContext c) {
            Instant timestamp = c.timestamp();
            for (String word : c.element().split("[^a-zA-Z']+")) {
                if (!word.isEmpty()) {
                    c.output(word + "| I was transformed and modified at: " + timestamp );
                }
            }
        }
    }

    public static void main(String[] args){

        PipelineOptionsFactory.register(BotDataFlowOptions.class);
        BotDataFlowOptions options = PipelineOptionsFactory.fromArgs(args)
                .withValidation().as(BotDataFlowOptions.class);

        options.setRunner(DataflowRunner.class);
        options.as(DataflowPipelineOptions.class).setStreaming(true);
        Pipeline p = Pipeline.create(options);

        FixedWindows window = FixedWindows.of(Duration.standardMinutes(
                options.getWindowSize()));

        p
                .apply(PubsubIO.readStrings().fromTopic(
                        options.getPubsubTopic()))
                .apply(Window.into(window))
                .apply(ParDo.of(new ExtractWordsFn()))
                .apply(TextIO.write().to(
                        options.getOutput()).withWindowedWrites().withNumShards(1));

        p.run().waitUntilFinish();


    }

}
