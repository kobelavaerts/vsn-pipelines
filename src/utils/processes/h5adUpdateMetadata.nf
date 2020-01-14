nextflow.preview.dsl=2

if(!params.containsKey("test")) {
    binDir = "${workflow.projectDir}/src/utils/bin/"
} else {
    binDir = ""
}

process SC__UTILS__UPDATE_FEATURE_METADATA_INDEX {

    container params.sc.scanpy.container
    publishDir "${params.global.outdir}/data/intermediate", mode: 'link', overwrite: true
    clusterOptions "-l nodes=1:ppn=2 -l walltime=1:00:00 -A ${params.global.qsubaccount}"

    input:
        tuple val(sampleId), path(f), path(additionalMetadata)

    output:
        tuple val(sampleId), path("${sampleId}.SC__UTILS__UPDATE_FEATURE_METADATA_INDEX.h5ad")

    script:
        def sampleParams = params.parseConfig(sampleId, params.global, params.utils.update_feature_metadata_index)
		processParams = sampleParams.local
        """
        ${binDir}sc_h5ad_update_metadata.py \
            --additional-metadata ${additionalMetadata} \
            --axis feature \
            --index-column-name ${processParams.indexColumnName} \
            --join-key ${processParams.joinKey} \
            $f \
            --output "${sampleId}.SC__UTILS__UPDATE_FEATURE_METADATA_INDEX.h5ad"
        """

}
