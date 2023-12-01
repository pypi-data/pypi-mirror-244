# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'InstancePlatform',
    'InstanceType',
    'PlacementStrategy',
    'ProtocolType',
    'Tenancy',
]


class InstancePlatform(str, Enum):
    LINUX_UNIX = "Linux/UNIX"
    RED_HAT_ENTERPRISE_LINUX = "Red Hat Enterprise Linux"
    SUSE_LINUX = "SUSE Linux"
    WINDOWS = "Windows"
    WINDOWS_WITH_SQL_SERVER = "Windows with SQL Server"
    WINDOWS_WITH_SQL_SERVER_ENTERPRISE = "Windows with SQL Server Enterprise"
    WINDOWS_WITH_SQL_SERVER_STANDARD = "Windows with SQL Server Standard"
    WINDOWS_WITH_SQL_SERVER_WEB = "Windows with SQL Server Web"


class InstanceType(str, Enum):
    A1_2_X_LARGE = "a1.2xlarge"
    A1_4_X_LARGE = "a1.4xlarge"
    A1_LARGE = "a1.large"
    A1_MEDIUM = "a1.medium"
    A1_METAL = "a1.metal"
    A1_X_LARGE = "a1.xlarge"
    C1_MEDIUM = "c1.medium"
    C1_X_LARGE = "c1.xlarge"
    C3_2_X_LARGE = "c3.2xlarge"
    C3_4_X_LARGE = "c3.4xlarge"
    C3_8_X_LARGE = "c3.8xlarge"
    C3_LARGE = "c3.large"
    C3_X_LARGE = "c3.xlarge"
    C4_2_X_LARGE = "c4.2xlarge"
    C4_4_X_LARGE = "c4.4xlarge"
    C4_8_X_LARGE = "c4.8xlarge"
    C4_LARGE = "c4.large"
    C4_X_LARGE = "c4.xlarge"
    C5_12_X_LARGE = "c5.12xlarge"
    C5_18_X_LARGE = "c5.18xlarge"
    C5_24_X_LARGE = "c5.24xlarge"
    C5_2_X_LARGE = "c5.2xlarge"
    C5_4_X_LARGE = "c5.4xlarge"
    C5_9_X_LARGE = "c5.9xlarge"
    C5_LARGE = "c5.large"
    C5_METAL = "c5.metal"
    C5_X_LARGE = "c5.xlarge"
    C5A_12_X_LARGE = "c5a.12xlarge"
    C5A_16_X_LARGE = "c5a.16xlarge"
    C5A_24_X_LARGE = "c5a.24xlarge"
    C5A_2_X_LARGE = "c5a.2xlarge"
    C5A_4_X_LARGE = "c5a.4xlarge"
    C5A_8_X_LARGE = "c5a.8xlarge"
    C5A_LARGE = "c5a.large"
    C5A_X_LARGE = "c5a.xlarge"
    C5AD_12_X_LARGE = "c5ad.12xlarge"
    C5AD_16_X_LARGE = "c5ad.16xlarge"
    C5AD_24_X_LARGE = "c5ad.24xlarge"
    C5AD_2_X_LARGE = "c5ad.2xlarge"
    C5AD_4_X_LARGE = "c5ad.4xlarge"
    C5AD_8_X_LARGE = "c5ad.8xlarge"
    C5AD_LARGE = "c5ad.large"
    C5AD_X_LARGE = "c5ad.xlarge"
    C5D_12_X_LARGE = "c5d.12xlarge"
    C5D_18_X_LARGE = "c5d.18xlarge"
    C5D_24_X_LARGE = "c5d.24xlarge"
    C5D_2_X_LARGE = "c5d.2xlarge"
    C5D_4_X_LARGE = "c5d.4xlarge"
    C5D_9_X_LARGE = "c5d.9xlarge"
    C5D_LARGE = "c5d.large"
    C5D_METAL = "c5d.metal"
    C5D_X_LARGE = "c5d.xlarge"
    C5N_18_X_LARGE = "c5n.18xlarge"
    C5N_2_X_LARGE = "c5n.2xlarge"
    C5N_4_X_LARGE = "c5n.4xlarge"
    C5N_9_X_LARGE = "c5n.9xlarge"
    C5N_LARGE = "c5n.large"
    C5N_METAL = "c5n.metal"
    C5N_X_LARGE = "c5n.xlarge"
    C6A_LARGE = "c6a.large"
    C6A_METAL = "c6a.metal"
    C6A_X_LARGE = "c6a.xlarge"
    C6A_2_X_LARGE = "c6a.2xlarge"
    C6A_4_X_LARGE = "c6a.4xlarge"
    C6A_8_X_LARGE = "c6a.8xlarge"
    C6A_12_X_LARGE = "c6a.12xlarge"
    C6A_16_X_LARGE = "c6a.16xlarge"
    C6A_24_X_LARGE = "c6a.24xlarge"
    C6A_32_X_LARGE = "c6a.32xlarge"
    C6A_48_X_LARGE = "c6a.48xlarge"
    C6G_12_X_LARGE = "c6g.12xlarge"
    C6G_16_X_LARGE = "c6g.16xlarge"
    C6G_2_X_LARGE = "c6g.2xlarge"
    C6G_4_X_LARGE = "c6g.4xlarge"
    C6G_8_X_LARGE = "c6g.8xlarge"
    C6G_LARGE = "c6g.large"
    C6G_MEDIUM = "c6g.medium"
    C6G_METAL = "c6g.metal"
    C6G_X_LARGE = "c6g.xlarge"
    C6GD_12_X_LARGE = "c6gd.12xlarge"
    C6GD_16_X_LARGE = "c6gd.16xlarge"
    C6GD_2_X_LARGE = "c6gd.2xlarge"
    C6GD_4_X_LARGE = "c6gd.4xlarge"
    C6GD_8_X_LARGE = "c6gd.8xlarge"
    C6GD_LARGE = "c6gd.large"
    C6GD_MEDIUM = "c6gd.medium"
    C6GD_METAL = "c6gd.metal"
    C6GD_X_LARGE = "c6gd.xlarge"
    C6I_LARGE = "c6i.large"
    C6I_X_LARGE = "c6i.xlarge"
    C6I_2_X_LARGE = "c6i.2xlarge"
    C6I_4_X_LARGE = "c6i.4xlarge"
    C6I_8_X_LARGE = "c6i.8xlarge"
    C6I_12_X_LARGE = "c6i.12xlarge"
    C6I_16_X_LARGE = "c6i.16xlarge"
    C6I_24_X_LARGE = "c6i.24xlarge"
    C6I_32_X_LARGE = "c6i.32xlarge"
    C6I_METAL = "c6i.metal"
    C6ID_LARGE = "c6id.large"
    C6ID_X_LARGE = "c6id.xlarge"
    C6ID_2_X_LARGE = "c6id.2xlarge"
    C6ID_4_X_LARGE = "c6id.4xlarge"
    C6ID_8_X_LARGE = "c6id.8xlarge"
    C6ID_12_X_LARGE = "c6id.12xlarge"
    C6ID_16_X_LARGE = "c6id.16xlarge"
    C6ID_24_X_LARGE = "c6id.24xlarge"
    C6ID_32_X_LARGE = "c6id.32xlarge"
    C6ID_METAL = "c6id.metal"
    CC2_8_X_LARGE = "cc2.8xlarge"
    D2_2_X_LARGE = "d2.2xlarge"
    D2_4_X_LARGE = "d2.4xlarge"
    D2_8_X_LARGE = "d2.8xlarge"
    D2_X_LARGE = "d2.xlarge"
    D3_2_X_LARGE = "d3.2xlarge"
    D3_4_X_LARGE = "d3.4xlarge"
    D3_8_X_LARGE = "d3.8xlarge"
    D3_X_LARGE = "d3.xlarge"
    D3EN_12_X_LARGE = "d3en.12xlarge"
    D3EN_2_X_LARGE = "d3en.2xlarge"
    D3EN_4_X_LARGE = "d3en.4xlarge"
    D3EN_6_X_LARGE = "d3en.6xlarge"
    D3EN_8_X_LARGE = "d3en.8xlarge"
    D3EN_X_LARGE = "d3en.xlarge"
    F1_16_X_LARGE = "f1.16xlarge"
    F1_2_X_LARGE = "f1.2xlarge"
    F1_4_X_LARGE = "f1.4xlarge"
    G2_2_X_LARGE = "g2.2xlarge"
    G2_8_X_LARGE = "g2.8xlarge"
    G3_16_X_LARGE = "g3.16xlarge"
    G3_4_X_LARGE = "g3.4xlarge"
    G3_8_X_LARGE = "g3.8xlarge"
    G3S_X_LARGE = "g3s.xlarge"
    G4AD_16_X_LARGE = "g4ad.16xlarge"
    G4AD_X_LARGE = "g4ad.xlarge"
    G4AD_2_X_LARGE = "g4ad.2xlarge"
    G4AD_4_X_LARGE = "g4ad.4xlarge"
    G4AD_8_X_LARGE = "g4ad.8xlarge"
    G4DN_12_X_LARGE = "g4dn.12xlarge"
    G4DN_16_X_LARGE = "g4dn.16xlarge"
    G4DN_2_X_LARGE = "g4dn.2xlarge"
    G4DN_4_X_LARGE = "g4dn.4xlarge"
    G4DN_8_X_LARGE = "g4dn.8xlarge"
    G4DN_METAL = "g4dn.metal"
    G4DN_X_LARGE = "g4dn.xlarge"
    H1_16_X_LARGE = "h1.16xlarge"
    H1_2_X_LARGE = "h1.2xlarge"
    H1_4_X_LARGE = "h1.4xlarge"
    H1_8_X_LARGE = "h1.8xlarge"
    I2_2_X_LARGE = "i2.2xlarge"
    I2_4_X_LARGE = "i2.4xlarge"
    I2_8_X_LARGE = "i2.8xlarge"
    I2_X_LARGE = "i2.xlarge"
    I3_16_X_LARGE = "i3.16xlarge"
    I3_2_X_LARGE = "i3.2xlarge"
    I3_4_X_LARGE = "i3.4xlarge"
    I3_8_X_LARGE = "i3.8xlarge"
    I3_LARGE = "i3.large"
    I3_X_LARGE = "i3.xlarge"
    I3_METAL = "i3.metal"
    I3EN_12_X_LARGE = "i3en.12xlarge"
    I3EN_24_X_LARGE = "i3en.24xlarge"
    I3EN_2_X_LARGE = "i3en.2xlarge"
    I3EN_3_X_LARGE = "i3en.3xlarge"
    I3EN_6_X_LARGE = "i3en.6xlarge"
    I3EN_LARGE = "i3en.large"
    I3EN_METAL = "i3en.metal"
    I3EN_X_LARGE = "i3en.xlarge"
    INF1_24_X_LARGE = "inf1.24xlarge"
    INF1_2_X_LARGE = "inf1.2xlarge"
    INF1_6_X_LARGE = "inf1.6xlarge"
    INF1_X_LARGE = "inf1.xlarge"
    M1_LARGE = "m1.large"
    M1_MEDIUM = "m1.medium"
    M1_SMALL = "m1.small"
    M1_X_LARGE = "m1.xlarge"
    M2_2_X_LARGE = "m2.2xlarge"
    M2_4_X_LARGE = "m2.4xlarge"
    M2_X_LARGE = "m2.xlarge"
    M3_2_X_LARGE = "m3.2xlarge"
    M3_LARGE = "m3.large"
    M3_MEDIUM = "m3.medium"
    M3_X_LARGE = "m3.xlarge"
    M4_10_X_LARGE = "m4.10xlarge"
    M4_16_X_LARGE = "m4.16xlarge"
    M4_2_X_LARGE = "m4.2xlarge"
    M4_4_X_LARGE = "m4.4xlarge"
    M4_LARGE = "m4.large"
    M4_X_LARGE = "m4.xlarge"
    M5_12_X_LARGE = "m5.12xlarge"
    M5_16_X_LARGE = "m5.16xlarge"
    M5_24_X_LARGE = "m5.24xlarge"
    M5_2_X_LARGE = "m5.2xlarge"
    M5_4_X_LARGE = "m5.4xlarge"
    M5_8_X_LARGE = "m5.8xlarge"
    M5_LARGE = "m5.large"
    M5_METAL = "m5.metal"
    M5_X_LARGE = "m5.xlarge"
    M5A_12_X_LARGE = "m5a.12xlarge"
    M5A_16_X_LARGE = "m5a.16xlarge"
    M5A_24_X_LARGE = "m5a.24xlarge"
    M5A_2_X_LARGE = "m5a.2xlarge"
    M5A_4_X_LARGE = "m5a.4xlarge"
    M5A_8_X_LARGE = "m5a.8xlarge"
    M5A_LARGE = "m5a.large"
    M5A_X_LARGE = "m5a.xlarge"
    M5AD_12_X_LARGE = "m5ad.12xlarge"
    M5AD_16_X_LARGE = "m5ad.16xlarge"
    M5AD_24_X_LARGE = "m5ad.24xlarge"
    M5AD_2_X_LARGE = "m5ad.2xlarge"
    M5AD_4_X_LARGE = "m5ad.4xlarge"
    M5AD_8_X_LARGE = "m5ad.8xlarge"
    M5AD_LARGE = "m5ad.large"
    M5AS_X_LARGE = "m5ad.xlarge"
    M5D_12_X_LARGE = "m5d.12xlarge"
    M5D_16_X_LARGE = "m5d.16xlarge"
    M5D_24_X_LARGE = "m5d.24xlarge"
    M5D_2_X_LARGE = "m5d.2xlarge"
    M5D_4_X_LARGE = "m5d.4xlarge"
    M5D_8_X_LARGE = "m5d.8xlarge"
    M5D_LARGE = "m5d.large"
    M5D_METAL = "m5d.metal"
    M5D_X_LARGE = "m5d.xlarge"
    M5DN_12_X_LARGE = "m5dn.12xlarge"
    M5DN_16_X_LARGE = "m5dn.16xlarge"
    M5DN_24_X_LARGE = "m5dn.24xlarge"
    M5DN_2_X_LARGE = "m5dn.2xlarge"
    M5DN_4_X_LARGE = "m5dn.4xlarge"
    M5DN_8_X_LARGE = "m5dn.8xlarge"
    M5DN_LARGE = "m5dn.large"
    M5DN_X_LARGE = "m5dn.xlarge"
    M5N_12_X_LARGE = "m5n.12xlarge"
    M5N_16_X_LARGE = "m5n.16xlarge"
    M5N_24_X_LARGE = "m5n.24xlarge"
    M5N_2_X_LARGE = "m5n.2xlarge"
    M5N_4_X_LARGE = "m5n.4xlarge"
    M5N_8_X_LARGE = "m5n.8xlarge"
    M5N_LARGE = "m5n.large"
    M5N_X_LARGE = "m5n.xlarge"
    M5ZN_12_X_LARGE = "m5zn.12xlarge"
    M5ZN_2_X_LARGE = "m5zn.2xlarge"
    M5ZN_3_X_LARGE = "m5zn.3xlarge"
    M5ZN_6_X_LARGE = "m5zn.6xlarge"
    M5ZN_LARGE = "m5zn.large"
    M5ZN_METAL = "m5zn.metal"
    M5ZN_X_LARGE = "m5zn.xlarge"
    M6A_LARGE = "m6a.large"
    M6A_METAL = "m6a.metal"
    M6A_X_LARGE = "m6a.xlarge"
    M6A_2_X_LARGE = "m6a.2xlarge"
    M6A_4_X_LARGE = "m6a.4xlarge"
    M6A_8_X_LARGE = "m6a.8xlarge"
    M6A_12_X_LARGE = "m6a.12xlarge"
    M6A_16_X_LARGE = "m6a.16xlarge"
    M6A_24_X_LARGE = "m6a.24xlarge"
    M6A_32_X_LARGE = "m6a.32xlarge"
    M6A_48_X_LARGE = "m6a.48xlarge"
    M6G_12_X_LARGE = "m6g.12xlarge"
    M6G_16_X_LARGE = "m6g.16xlarge"
    M6G_2_X_LARGE = "m6g.2xlarge"
    M6G_4_X_LARGE = "m6g.4xlarge"
    M6G_8_X_LARGE = "m6g.8xlarge"
    M6G_LARGE = "m6g.large"
    M6G_MEDIUM = "m6g.medium"
    M6G_METAL = "m6g.metal"
    M6G_X_LARGE = "m6g.xlarge"
    M6GD_12_X_LARGE = "m6gd.12xlarge"
    M6GD_16_X_LARGE = "m6gd.16xlarge"
    M6GD_2_X_LARGE = "m6gd.2xlarge"
    M6GD_4_X_LARGE = "m6gd.4xlarge"
    M6GD_8_X_LARGE = "m6gd.8xlarge"
    M6GD_LARGE = "m6gd.large"
    M6GD_MEDIUM = "m6gd.medium"
    M6GD_METAL = "m6gd.metal"
    M6GD_X_LARGE = "m6gd.xlarge"
    M6I_LARGE = "m6i.large"
    M6I_X_LARGE = "m6i.xlarge"
    M6I_2_X_LARGE = "m6i.2xlarge"
    M6I_4_X_LARGE = "m6i.4xlarge"
    M6I_8_X_LARGE = "m6i.8xlarge"
    M6I_12_X_LARGE = "m6i.12xlarge"
    M6I_16_X_LARGE = "m6i.16xlarge"
    M6I_24_X_LARGE = "m6i.24xlarge"
    M6I_32_X_LARGE = "m6i.32xlarge"
    M6I_METAL = "m6i.metal"
    M6ID_LARGE = "m6id.large"
    M6ID_X_LARGE = "m6id.xlarge"
    M6ID_2_X_LARGE = "m6id.2xlarge"
    M6ID_4_X_LARGE = "m6id.4xlarge"
    M6ID_8_X_LARGE = "m6id.8xlarge"
    M6ID_12_X_LARGE = "m6id.12xlarge"
    M6ID_16_X_LARGE = "m6id.16xlarge"
    M6ID_24_X_LARGE = "m6id.24xlarge"
    M6ID_32_X_LARGE = "m6id.32xlarge"
    M6ID_METAL = "m6id.metal"
    M7A_MEDIUM = "m7a.medium"
    M7A_LARGE = "m7a.large"
    M7A_X_LARGE = "m7a.xlarge"
    M7A_2_X_LARGE = "m7a.2xlarge"
    M7A_4_X_LARGE = "m7a.4xlarge"
    M7A_8_X_LARGE = "m7a.8xlarge"
    M7A_12_X_LARGE = "m7a.12xlarge"
    M7A_16_X_LARGE = "m7a.16xlarge"
    M7A_24_X_LARGE = "m7a.24xlarge"
    M7A_32_X_LARGE = "m7a.32xlarge"
    M7A_48_X_LARGE = "m7a.48xlarge"
    M7A_METAL = "m7a.metal-48xl"
    MAC1_METAL = "mac1.metal"
    P2_16_X_LARGE = "p2.16xlarge"
    P2_8_X_LARGE = "p2.8xlarge"
    P2_X_LARGE = "p2.xlarge"
    P3_16_X_LARGE = "p3.16xlarge"
    P3_2_X_LARGE = "p3.2xlarge"
    P3_8_X_LARGE = "p3.8xlarge"
    P3DN_24_X_LARGE = "p3dn.24xlarge"
    P4D_24_X_LARGE = "p4d.24xlarge"
    R3_2_X_LARGE = "r3.2xlarge"
    R3_4_X_LARGE = "r3.4xlarge"
    R3_8_X_LARGE = "r3.8xlarge"
    R3_LARGE = "r3.large"
    R3_X_LARGE = "r3.xlarge"
    R4_16_X_LARGE = "r4.16xlarge"
    R4_2_X_LARGE = "r4.2xlarge"
    R4_4_X_LARGE = "r4.4xlarge"
    R4_8_X_LARGE = "r4.8xlarge"
    R4_LARGE = "r4.large"
    R4_X_LARGE = "r4.xlarge"
    R5_12_X_LARGE = "r5.12xlarge"
    R5_16_X_LARGE = "r5.16xlarge"
    R5_24_X_LARGE = "r5.24xlarge"
    R5_2_X_LARGE = "r5.2xlarge"
    R5_4_X_LARGE = "r5.4xlarge"
    R5_8_X_LARGE = "r5.8xlarge"
    R5_LARGE = "r5.large"
    R5_METAL = "r5.metal"
    R5_X_LARGE = "r5.xlarge"
    R5A_12_X_LARGE = "r5a.12xlarge"
    R5A_16_X_LARGE = "r5a.16xlarge"
    R5A_24_X_LARGE = "r5a.24xlarge"
    R5A_2_X_LARGE = "r5a.2xlarge"
    R5A_4_X_LARGE = "r5a.4xlarge"
    R5A_8_X_LARGE = "r5a.8xlarge"
    R5A_LARGE = "r5a.large"
    R5A_X_LARGE = "r5a.xlarge"
    R5AD_12_X_LARGE = "r5ad.12xlarge"
    R5AD_16_X_LARGE = "r5ad.16xlarge"
    R5AD_24_X_LARGE = "r5ad.24xlarge"
    R5AD_2_X_LARGE = "r5ad.2xlarge"
    R5AD_4_X_LARGE = "r5ad.4xlarge"
    R5AD_8_X_LARGE = "r5ad.8xlarge"
    R5AD_LARGE = "r5ad.large"
    R5AD_X_LARGE = "r5ad.xlarge"
    R5B_12_X_LARGE = "r5b.12xlarge"
    R5B_16_X_LARGE = "r5b.16xlarge"
    R5B_24_X_LARGE = "r5b.24xlarge"
    R5B_2_X_LARGE = "r5b.2xlarge"
    R5B_4_X_LARGE = "r5b.4xlarge"
    R5B_8_X_LARGE = "r5b.8xlarge"
    R5B_LARGE = "r5b.large"
    R5B_METAL = "r5b.metal"
    R5B_X_LARGE = "r5b.xlarge"
    R5D_12_X_LARGE = "r5d.12xlarge"
    R5D_16_X_LARGE = "r5d.16xlarge"
    R5D_24_X_LARGE = "r5d.24xlarge"
    R5D_2_X_LARGE = "r5d.2xlarge"
    R5D_4_X_LARGE = "r5d.4xlarge"
    R5D_8_X_LARGE = "r5d.8xlarge"
    R5D_LARGE = "r5d.large"
    R5D_METAL = "r5d.metal"
    R5D_X_LARGE = "r5d.xlarge"
    R5DN_12_X_LARGE = "r5dn.12xlarge"
    R5DN_16_X_LARGE = "r5dn.16xlarge"
    R5DN_24_X_LARGE = "r5dn.24xlarge"
    R5DN_2_X_LARGE = "r5dn.2xlarge"
    R5DN_4_X_LARGE = "r5dn.4xlarge"
    R5DN_8_X_LARGE = "r5dn.8xlarge"
    R5DN_LARGE = "r5dn.large"
    R5DN_X_LARGE = "r5dn.xlarge"
    R5N_12_X_LARGE = "r5n.12xlarge"
    R5N_16_X_LARGE = "r5n.16xlarge"
    R5N_24_X_LARGE = "r5n.24xlarge"
    R5N_2_X_LARGE = "r5n.2xlarge"
    R5N_4_X_LARGE = "r5n.4xlarge"
    R5N_8_X_LARGE = "r5n.8xlarge"
    R5N_LARGE = "r5n.large"
    R5N_X_LARGE = "r5n.xlarge"
    R6G_12_X_LARGE = "r6g.12xlarge"
    R6G_16_X_LARGE = "r6g.16xlarge"
    R6G_2_X_LARGE = "r6g.2xlarge"
    R6G_4_X_LARGE = "r6g.4xlarge"
    R6G_8_X_LARGE = "r6g.8xlarge"
    R6G_LARGE = "r6g.large"
    R6G_MEDIUM = "r6g.medium"
    R6G_METAL = "r6g.metal"
    R6G_X_LARGE = "r6g.xlarge"
    R6GD_12_X_LARGE = "r6gd.12xlarge"
    R6GD_16_X_LARGE = "r6gd.16xlarge"
    R6GD_2_X_LARGE = "r6gd.2xlarge"
    R6GD_4_X_LARGE = "r6gd.4xlarge"
    R6GD_8_X_LARGE = "r6gd.8xlarge"
    R6GD_LARGE = "r6gd.large"
    R6GD_MEDIUM = "r6gd.medium"
    R6GD_METAL = "r6gd.metal"
    R6GD_X_LARGE = "r6gd.xlarge"
    R6I_LARGE = "r6i.large"
    R6I_X_LARGE = "r6i.xlarge"
    R6I_2_X_LARGE = "r6i.2xlarge"
    R6I_4_X_LARGE = "r6i.4xlarge"
    R6I_8_X_LARGE = "r6i.8xlarge"
    R6I_12_X_LARGE = "r6i.12xlarge"
    R6I_16_X_LARGE = "r6i.16xlarge"
    R6I_24_X_LARGE = "r6i.24xlarge"
    R6I_32_X_LARGE = "r6i.32xlarge"
    R6I_METAL = "r6i.metal"
    R6ID_LARGE = "r6id.large"
    R6ID_X_LARGE = "r6id.xlarge"
    R6ID_2_X_LARGE = "r6id.2xlarge"
    R6ID_4_X_LARGE = "r6id.4xlarge"
    R6ID_8_X_LARGE = "r6id.8xlarge"
    R6ID_12_X_LARGE = "r6id.12xlarge"
    R6ID_16_X_LARGE = "r6id.16xlarge"
    R6ID_24_X_LARGE = "r6id.24xlarge"
    R6ID_32_X_LARGE = "r6id.32xlarge"
    R6ID_METAL = "r6id.metal"
    T1_MICRO = "t1.micro"
    T2_2_X_LARGE = "t2.2xlarge"
    T2_LARGE = "t2.large"
    T2_MEDIUM = "t2.medium"
    T2_MICRO = "t2.micro"
    T2_NANO = "t2.nano"
    T2_SMALL = "t2.small"
    T2_X_LARGE = "t2.xlarge"
    T3_2_X_LARGE = "t3.2xlarge"
    T3_LARGE = "t3.large"
    T3_MEDIUM = "t3.medium"
    T3_MICRO = "t3.micro"
    T3_NANO = "t3.nano"
    T3_SMALL = "t3.small"
    T3_X_LARGE = "t3.xlarge"
    T3A_2_X_LARGE = "t3a.2xlarge"
    T3A_LARGE = "t3a.large"
    T3A_MEDIUM = "t3a.medium"
    T3A_MICRO = "t3a.micro"
    T3A_NANO = "t3a.nano"
    T3A_SMALL = "t3a.small"
    T3A_X_LARGE = "t3a.xlarge"
    T4G_2_X_LARGE = "t4g.2xlarge"
    T4G_LARGE = "t4g.large"
    T4G_MEDIUM = "t4g.medium"
    T4G_MICRO = "t4g.micro"
    T4G_NANO = "t4g.nano"
    T4G_SMALL = "t4g.small"
    T4G_X_LARGE = "t4g.xlarge"
    X1_16_X_LARGE = "x1.16xlarge"
    X1_32_X_LARGE = "x1.32xlarge"
    X1E_16_X_LARGE = "x1e.16xlarge"
    X1E_2_X_LARGE = "x1e.2xlarge"
    X1E_32_X_LARGE = "x1e.32xlarge"
    X1E_4_X_LARGE = "x1e.4xlarge"
    X1E_8_X_LARGE = "x1e.8xlarge"
    X1E_X_LARGE = "x1e.xlarge"
    Z1D_12_X_LARGE = "z1d.12xlarge"
    Z1D_2_X_LARGE = "z1d.2xlarge"
    Z1D_3_X_LARGE = "z1d.3xlarge"
    Z1D_6_X_LARGE = "z1d.6xlarge"
    Z1D_LARGE = "z1d.large"
    Z1D_METAL = "z1d.metal"
    Z1D_X_LARGE = "z1d.xlarge"
    U_12TB1_METAL = "u-12tb1.metal"
    U_6TB1_METAL = "u-6tb1.metal"
    U_9TB1_METAL = "u-9tb1.metal"
    HS1_8_X_LARGE = "hs1.8xlarge"


class PlacementStrategy(str, Enum):
    """
    The strategy of the placement group determines how the instances are organized within the group.
    See https://docs.aws.amazon.com/cli/latest/reference/ec2/create-placement-group.html
    """
    SPREAD = "spread"
    """
    A `spread` placement group places instances on distinct hardware.
    """
    CLUSTER = "cluster"
    """
    A `cluster` placement group is a logical grouping of instances within a single
    Availability Zone that benefit from low network latency, high network throughput.
    """


class ProtocolType(str, Enum):
    ALL = "all"
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"


class Tenancy(str, Enum):
    DEFAULT = "default"
    DEDICATED = "dedicated"
