from passlib.context import CryptContext

crypto_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_sequence(source_sequence: str, target_sequence_hash: str) -> bool:
    return crypto_context.verify(source_sequence, target_sequence_hash)


def get_hash(sequence: str) -> str:
    return crypto_context.hash(sequence)
