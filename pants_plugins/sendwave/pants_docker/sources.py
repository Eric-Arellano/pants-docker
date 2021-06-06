from dataclasses import dataclass
from pants.engine.unions import UnionRule
from pants.build_graph.address import AddressInput
from pants.engine.rules import collect_rules, rule, Get, MultiGet
from pants.core.util_rules.stripped_source_files import StrippedSourceFiles
from pants.core.util_rules.source_files import SourceFiles, SourceFilesRequest
from pants.backend.python.target_types import PythonSources
from pants.engine.target import  Sources, FieldSet
from pants.core.target_types import (ResourcesSources, FilesSources)

from pants.engine.fs import Digest, RemovePrefix, Snapshot
from sendwave.pants_docker.docker_component import DockerComponentRequest, DockerComponent
from sendwave.pants_docker.target import StripPrefixSources, PrefixToStrip

@dataclass(frozen=True)
class DockerStripPrefixFiles(FieldSet):
    required_fields = (StripPrefixSources, PrefixToStrip)
    sources: StripPrefixSources
    prefix: PrefixToStrip
        


class DockerStripPrefixFilesRequest(DockerComponentRequest):
    field_set_type = DockerStripPrefixFiles


@rule
async def get_stripped_prefix_files(req: DockerStripPrefixFiles) -> DockerComponent:
    # snapshot = await Get(SourceFiles, SourceFilesRequest([req.fs.sources]))
    # digest = await Get(Digest, RemovePrefix(snapshot.digest, req.fs.prefix))
    
    # print((await Get(Snapshot, Digest, digest)).files)
    return DockerComponent(commands=(),
                           sources=snapshot.digest)


@dataclass(frozen=True)
class DockerFiles(FieldSet):
    required_fields = (FilesSources,)
    sources: FilesSources


class DockerFilesRequest(DockerComponentRequest):
    field_set_type = DockerFiles

@rule
async def get_files(req: DockerFilesRequest) -> DockerComponent:
    return DockerComponent(commands=(),
                           sources=(await Get(SourceFiles,
                                              SourceFilesRequest([req.fs.sources]))).snapshot.digest)

@dataclass(frozen=True)
class DockerResources(FieldSet):
    required_fields = (ResourcesSources,)
    sources: ResourcesSources

class DockerResourcesRequest(DockerComponentRequest):
    field_set_type = DockerResources

@rule
async def get_resources(req: DockerResourcesRequest) -> DockerComponent:
    return DockerComponent(commands=(),
                           sources=(await Get(SourceFiles,
                                              SourceFilesRequest([req.fs.sources]))).snapshot.digest)

@dataclass(frozen=True)
class DockerPythonSources(FieldSet):
    required_fields = (PythonSources,)
    sources: PythonSources

class DockerPythonSourcesRequest(DockerComponentRequest):
    field_set_type = DockerPythonSources


@rule
async def get_sources(req: DockerPythonSourcesRequest) -> DockerComponent:
    source_files = await Get(StrippedSourceFiles,
                             SourceFilesRequest([req.fs.sources]))
    return DockerComponent(
        commands=(),
        sources=source_files.snapshot.digest)


def rules():
    return [UnionRule(DockerComponentRequest, DockerPythonSourcesRequest),
            UnionRule(DockerComponentRequest, DockerResourcesRequest),
            UnionRule(DockerComponentRequest, DockerFilesRequest),
            UnionRule(DockerComponentRequest, DockerStripPrefixFilesRequest),
            get_stripped_prefix_files,
            get_resources,
            get_files]
