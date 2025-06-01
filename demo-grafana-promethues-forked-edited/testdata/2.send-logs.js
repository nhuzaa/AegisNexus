import { check } from "k6";
import loki from "k6/x/loki";

let labels = loki.Labels({
  format: ["logfmt"],
  detected_level: ["error", "warn", "info"], // Added multiple status types
  instance: ["service1", "service2", "service3"],
  service_name: ["frontend", "backend", "payment", "inventory", "shipping"],
});

// Example query:
// count_over_time({detected_level="error", service_name=~".*"}[1m])

const conf = new loki.Config(
  __ENV.K6_LOKI_URL || "http://loki:3100/loki/api/v1/push",
  10000,
  1.0,
  { "X-Scope-OrgID": "single-tenant" }, // Explicitly set tenant ID
  labels
);

const client = new loki.Client(conf);

export default () => {
  // push random data (~800-900 log lines) according to the labels
  const res = client.push();
  check(res, { "successful write": (res) => res.status == 204 });
};
