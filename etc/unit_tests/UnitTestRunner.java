import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.fge.jsonpatch.diff.JsonDiff;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.io.FileUtils;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.ResultSet;
import org.apache.jena.query.ResultSetFormatter;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.ModelFactory;
import org.yaml.snakeyaml.Yaml;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Map;

public class UnitTestRunner {

    public static void main(String[] args) {
        try {
            Options options = createOptions();
            CommandLine cmd = parseCommandLine(args, options);

            String ontologyLocation = cmd.getOptionValue("ontology_location");
            String rootFolder = cmd.getOptionValue("root_folder");
            String cqSource = cmd.getOptionValue("cq_source");
            String configFilePath = cmd.getOptionValue("config_file");

            copyCqTemplates(cqSource, rootFolder);

            boolean cqTestsPassed = runUnitTest(ontologyLocation, rootFolder, configFilePath);

            System.exit(cqTestsPassed ? 0 : -1);
        } catch (ParseException e) {
            System.err.println("Error parsing command line arguments: " + e.getMessage());
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    private static Options createOptions() {
        Options options = new Options();
        options.addOption("ontology_location", true, "Path to ontology location");
        options.addOption("root_folder", true, "Path to the root folder");
        options.addOption("cq_source", true, "Path to the sources of cq templates");
        options.addOption("config_file", true, "Path to the config of test definition");
        return options;
    }

    private static CommandLine parseCommandLine(String[] args, Options options) throws ParseException {
        CommandLineParser parser = new DefaultParser();
        return parser.parse(options, args);
    }

    private static void copyCqTemplates(String cqSource, String rootFolder) throws IOException {
        FileUtils.copyDirectory(new File(cqSource), new File(rootFolder + "/cq_templates/"));
    }

    private static boolean runUnitTest(String ontologyLocation, String rootFolder, String unitTestConfigFilePath) throws IOException {
        Model ontology = ModelFactory.createDefaultModel();

        long startTime = System.currentTimeMillis();
        ontology.read(ontologyLocation);
        long endTime = System.currentTimeMillis();
        long elapsedTime = endTime - startTime;
        System.out.println("Parsing ontology " + ontologyLocation + " took " + elapsedTime / 1000.0 + " seconds");

        Map<String, Object> unitTestsConfig = getUnitTestsConfig(unitTestConfigFilePath, rootFolder);
        boolean cqTestsPassed = true;

        for (Map.Entry<String, Object> entry : unitTestsConfig.entrySet()) {
            String unitTestName = entry.getKey();
            Map<String, Object> unitTestConfig = (Map<String, Object>) entry.getValue();
            String sparqlQuery = getSparqlQuery(unitTestConfig, rootFolder);

            String queryResultString;
            try (QueryExecution queryExecution = QueryExecutionFactory.create(sparqlQuery, ontology); ByteArrayOutputStream outputStream = new ByteArrayOutputStream()) {
                ResultSet queryResult = queryExecution.execSelect();
                ResultSetFormatter.outputAsJSON(outputStream, queryResult);
                queryResultString = outputStream.toString();
            }

            String expectedOutputPath = (String) unitTestConfig.get("expected_output");
            String expectedOutput = readFileAsString(expectedOutputPath);

            if (!isResultExpected(queryResultString, expectedOutput)) {
                System.out.println("Competency question " + unitTestName + " run as a unit test failed.");
                cqTestsPassed = false;
            } else {
                System.out.println("Competency question " + unitTestName + " run as a unit test passed.");
            }
        }

        return cqTestsPassed;
    }

    private static Map<String, Object> getUnitTestsConfig(String unitTestConfigFilePath, String rootFolder) throws IOException {
        try (InputStream input = new FileInputStream(new File(rootFolder, unitTestConfigFilePath))) {
            Yaml yaml = new Yaml();
            return yaml.load(input);
        }
    }

    private static String getSparqlQuery(Map<String, Object> config, String rootFolder) throws IOException {
        String sparqlTemplatePath = (String) config.get("sparql_template");
        @SuppressWarnings("unchecked") Map<String, String> sparqlParameters = (Map<String, String>) config.get("parameters");
        String sparqlQuery = readFileAsString(new File(rootFolder, sparqlTemplatePath).getPath());

        for (Map.Entry<String, String> entry : sparqlParameters.entrySet()) {
            String sparqlParameter = entry.getKey();
            String sparqlParameterValue = entry.getValue();
            if (sparqlParameterValue.startsWith("<") && sparqlParameterValue.endsWith(">")) {
                sparqlQuery = sparqlQuery.replace(sparqlParameter, sparqlParameterValue);
            } else {
                sparqlQuery = sparqlQuery.replace(sparqlParameter, "\"" + sparqlParameterValue + "\"");
            }
        }

        return sparqlQuery;
    }

    private static boolean isResultExpected(String actual, String expected) {
        ObjectMapper objectMapper = new ObjectMapper();

        try {
            JsonNode actualJson = objectMapper.readTree(actual);
            JsonNode expectedJson = objectMapper.readTree(expected);

            JsonNode diff = JsonDiff.asJson(actualJson, expectedJson);

            if (diff.size() > 0) {
                System.out.println("Differences found:");
                System.out.println(diff);
                return false;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }

    private static String readFileAsString(String filePath) throws IOException {
        return Files.readString(Paths.get(filePath));
    }

}
