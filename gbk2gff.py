#!/usr/bin/env python
# coding: utf-8

import logging
import os
import sys
from pathlib import Path
from typing import Iterable, Optional, Union

import typer
from BCBio import GFF
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqFeature import CompoundLocation, FeatureLocation, SeqFeature
from Bio.SeqRecord import SeqRecord

__version__ = "0.1.0"
app = typer.Typer()

logger = logging.getLogger(__name__)


def init_logging(level: int):
    from rich.logging import RichHandler
    from rich.traceback import install

    install(show_locals=True, width=120, word_wrap=True)
    logging.basicConfig(
        format="%(message)s",
        datefmt="[%Y-%m-%d %X]",
        level=level,
        handlers=[RichHandler(rich_tracebacks=True, tracebacks_show_locals=True)],
    )


def version_callback(value: bool):
    if value:
        typer.echo(f"gbk2gff version {__version__}")
        raise typer.Exit()


def write_gff(gff_recs: list[SeqRecord], out_file: os.PathLike) -> None:
    """Write out GFF file"""
    with open(out_file, "w") as out_handle:
        GFF.write(gff_recs, out_handle)


def check_gff(gff_iterator: Iterable[SeqRecord], molecule_type: str = "DNA"):
    """Check GFF files before feeding to SeqIO to be sure they have sequences.

    source: https://github.com/chapmanb/bcbb/blob/81442c07173aaa59cbc1be33dd4a6e0eee87c5f6/gff/Scripts/gff/gff_to_genbank.py#L43
    """
    for rec in gff_iterator:
        if "molecule_type" not in rec.annotations:
            rec.annotations["molecule_type"] = molecule_type
        yield flatten_features(rec)


def flatten_features(rec: SeqRecord) -> SeqRecord:
    """Make sub_features in an input rec flat for output.

    GenBank does not handle nested features, so we want to make
    everything top level.

    source: https://github.com/chapmanb/bcbb/blob/81442c07173aaa59cbc1be33dd4a6e0eee87c5f6/gff/Scripts/gff/gff_to_genbank.py#L52
    """
    out = []
    for feature in rec.features:
        features = [feature]
        while features:
            next_features = []
            for current_feature in features:
                out.append(current_feature)
                if not hasattr(current_feature, "sub_features"):
                    continue
                new_features = []
                sub_features: Optional[list[SeqFeature]] = current_feature.sub_features
                if sub_features:
                    cds_subfeatures = [x for x in sub_features if x.type == "CDS"]
                    if len(cds_subfeatures) > 1:
                        subf = cds_subfeatures[0]
                        locations = [x.location for x in cds_subfeatures]
                        new_location = CompoundLocation(locations)
                        subf.location = new_location
                        subf.qualifiers["translation"] = [get_translation(rec.seq, new_location)]
                        new_features.append(subf)
                    else:
                        subf = cds_subfeatures[0]
                        subf.qualifiers["translation"] = [get_translation(rec.seq, subf.location)]
                        new_features.append(subf)
                    for subf in sub_features:
                        if subf.type == "signal_peptide_region_of_CDS":
                            subf.type = "sig_peptide"
                        elif subf.type == "mature_protein_region_of_CDS":
                            subf.type = "mat_peptide"
                        else:
                            continue
                        subf.qualifiers["translation"] = [get_translation(rec.seq, subf.location)]
                        try:
                            subf.qualifiers["gene"] = [feature.qualifiers["gene"][0]]
                        except KeyError:
                            pass
                        try:
                            subf.qualifiers["product"] = [feature.qualifiers["product"][0]]
                        except KeyError:
                            pass
                        new_features.append(subf)
                    next_features.extend(new_features)
            features = next_features
    rec.features = out
    return rec


def get_translation(seq: Seq, location: Union[FeatureLocation, CompoundLocation]) -> str:
    """Get translation of sequence from start to end"""
    translation = location.extract(seq).translate()
    if translation[-1] == "*":
        translation = translation[:-1]
    return translation


@app.command(
    epilog=f"gbk2gff version {__version__}; Python {sys.version_info.major}.{sys.version_info.minor}."
           f"{sys.version_info.micro}"
)
def main(
        input_gbk: Path = typer.Argument(..., exists=True, dir_okay=False, help="GenBank file to convert to GFF"),
        output_gff: Path = typer.Argument(..., help="Output GFF file"),
        version: Optional[bool] = typer.Option(  # noqa: ARG001
            None,
            "--version",
            "-V",
            callback=version_callback,
            help=f"Print 'gbk2gff version {__version__}' and exit",
        ),
):
    recs = list(SeqIO.parse(input_gbk, 'genbank'))
    rec = recs[0]
    rec = flatten_features(rec)
    write_gff([rec], output_gff)


if __name__ == "__main__":
    app()
