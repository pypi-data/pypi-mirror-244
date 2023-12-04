# A10's Thunder Observability Agent (TOA) - v2.0.0
	The TOA is a lightweight autonomous data processing engine that can be externally installed and configured for any Thunder device.
	TOA offers the following capabilities on Application Delivery Controller (ADC):
	
	- Collects, processes and publishes Thunder metrics. 
	  The default data collection frequency is 1 minute. 
	  Thunder metrics can be sent to the platform where Thunder is deployed, which includes AWS, Azure, and VMware or can be sent to shared platforms like Elasticsearch (Kibana), Prometheus (Grafana), and Splunk. 
	  Metrics can be sent to any one platform at a time. For more information on Thunder metrics, see Supported Thunder Metrics.

	
	- Collects, processes, and publishes Thunder Syslogs. 
	  The default data collection frequency is 1 minute. 
	  The logs can be published on various platforms like AWS, Azure, VMware, Kibana (Elasticsearch), Grafana (Prometheus and Pushgateway), or Splunk. 
      Logs can be sent to any one platform at a time. For more information on Thunder logs, see Supported Thunder Logs.

    Supported Monitoring Platforms:
	1. AWS.
	2. Azure.
	3. VMware.
	4. Splunk
	5. ElasticSearch-Kibana
	6. Prometheus-Grafana [PushGateway]

	Supported Use Cases:
	1. Monitoring thunder adc metrics or logs or both into AWS Cloudwatch.
	2. Monitoring thunder adc metrics or logs or both into Azure Application Insight and Log Analytics Workspace.
	3. Monitoring thunder adc metrics or logs or both into VMware vRealize Operations and Log Insight.
	4. Monitoring thunder adc metrics or logs or both into Splunk Console.
	5. Monitoring thunder adc metrics or logs or both into ElasticSearch/Kibana Console.
	6. Monitoring thunder adc metrics or logs or both into Prometheus/Grafana Console using PushGateway.
	

	Links:
	License				: https://www.a10networks.com/wp-content/uploads/EULA_Thunder_Observability_Agent.pdf
	Open Source (Notice)            : https://github.com/a10networks/thunder-observability-agent/tree/release/v2.0.0/OPEN-SOURCE-DISCLAIMER.pdf
	Documentation		        : https://documentation.a10networks.com/docs/Install/Software/thunder-observability-agent/
	Repository			: https://github.com/a10networks/thunder-observability-agent/tree/release/v2.0.0
	Example				: https://github.com/a10networks/thunder-observability-agent/tree/release/v2.0.0/examples
	
	
