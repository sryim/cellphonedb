from sqlalchemy import Column, Integer, String, ForeignKey

from cellcommdb.extensions import db


class Gene(db.Model):
    __tablename__ = 'gene'
    id_gene = Column(Integer, nullable=False, primary_key=True)

    ensembl = Column(String, nullable=False)
    gene_name = Column(String, nullable=False)

    protein_id = Column(Integer, ForeignKey('protein.id_protein'))
