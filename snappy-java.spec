Name:             snappy-java
Version:          1.0.4.1
Release:          7%{?dist}
Summary:          Fast compressor/decompresser
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://code.google.com/p/snappy-java

# hg clone --insecure -r snappy-java-1.0.4.1 https://code.google.com/p/snappy-java/
# cd snappy-java && hg archive -p snappy-java-1.0.4.1/ -X 'lib/*.jar' -t tgz ../snappy-java-1.0.4.1-CLEAN.tgz
Source0:          snappy-java-%{version}-CLEAN.tgz

Patch0:           snappy-java-%{version}-pom.patch

BuildArch:        noarch

BuildRequires:    felix-osgi-core
BuildRequires:    java-devel
BuildRequires:    jboss-logging
BuildRequires:    jpackage-utils
BuildRequires:    maven-local
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-install-plugin
BuildRequires:    maven-jar-plugin
BuildRequires:    maven-javadoc-plugin

Requires:         felix-osgi-core
Requires:         jboss-logging
Requires:         jpackage-utils

%description
A Java port of the snappy, a fast compresser/decompresser written in C++.

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation
Requires:         jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

%patch0 -p1

%build
# no xerial package available
mvn-rpmbuild -Dmaven.test.skip=true install javadoc:aggregate

%install
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# JAR
install -pm 644 target/snappy-java-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# POM
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# DEPMAP
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# APIDOCS
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*
%doc LICENSE README NOTICE

%files javadoc
%{_javadocdir}/%{name}
%doc LICENSE

%changelog
* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 1.0.4.1-7
- Use Requires: java-headless rebuild (#1067528)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.4.1-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 4 2012 Ricardo Arguello <ricardo@fedoraproject.org> 1.0.4.1-2
- Cleanup of the spec file

* Tue Feb 21 2012 Marek Goldmann <mgoldman@redhat.com> 1.0.4.1-1
- Initial packaging
