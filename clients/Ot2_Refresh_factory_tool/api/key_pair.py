from dataclasses import dataclass
import hashlib
import paramiko


@dataclass()
class keyPair:

    public: str

    private: paramiko.PKey

    @property
    def public_id(self)->str:
        """The ID that the public key will have when it's installed on an OT-2."""
        # Strip just a single trailing newline to match how we hash keys on the
        # robot side.
        if self.public[-1] == "\n":
            to_hash = self.public[:-1]
        else:
            to_hash = self.public
        return hashlib.new("md5", to_hash.encode()).hexdigest()


    @classmethod
    def generate(cls):
        """Generate a brand-new SSH key pair compatible with the OT-2."""
        # We want this to be big enough to resist sustained attack in case, for
        # whatever reason, this key isn't removed from the OT-2 before the OT-2 leaves
        # the factory.
        private = paramiko.RSAKey.generate(bits=4096)

        key_type = private.get_name()
        base64_key = private.get_base64()
        comment = "ot2-factory-tools"
        public = f"{key_type} {base64_key} {comment}"

        return cls(public=public,private=private)


# if __name__ == '__main__':
#     keyPair.generate()


